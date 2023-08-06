import io
import os
from enum import Enum
from typing import Optional, Tuple, Union

import torch
from omegaconf import DictConfig, OmegaConf

from comfy.hazard.sd import load_checkpoint as _load_checkpoint, ModelPatcher, load_checkpoint_guess_config as _load_checkpoint_guess_config
from comfy.clip import CLIPModel
from comfy.conditioning import Conditioning
from comfy.hazard.ldm.models.diffusion.ddpm import LatentDiffusion
from comfy.hazard.nodes import common_ksampler
from comfy.latent_image import LatentImage
from comfy.util import ModelLoadError, SDType
from comfy.vae import VAEModel


class SDVersion(Enum):
    SD1x = "SD1.x"
    SD2x = "SD2.x"


class Sampler(Enum):
    SAMPLE_EULER = "sample_euler"
    SAMPLE_EULER_ANCESTRAL = "sample_euler_ancestral"
    SAMPLE_HEUN = "sample_heun"
    SAMPLE_DPM_2 = "sample_dpm_2"
    SAMPLE_DPM_2_ANCESTRAL = "sample_dpm_2_ancestral"
    SAMPLE_LMS = "sample_lms"
    SAMPLE_DPM_FAST = "sample_dpm_fast"
    SAMPLE_DPM_ADAPTIVE = "sample_dpm_adaptive"
    SAMPLE_DPMpp_2S_ANCESTRAL = "sample_dpmpp_2s_ancestral"
    SAMPLE_DPMpp_SDE = "sample_dpmpp_sde"
    SAMPLE_DPMpp_2M = "sample_dpmpp_2m"
    DDIM = "ddim"
    UNI_PC = "uni_pc"
    UNI_PC_BH2 = "uni_pc_bh2"


class Scheduler(Enum):
    KARRAS = "karras"
    NORMAL = "normal"
    SIMPLE = "simple"
    DDIM_UNIFORM = "ddim_uniform"


class BuiltInCheckpointConfigName(Enum):
    V1 = "v1-inference.yaml"
    V2 = "v2-inference.yaml"


class CheckpointConfig:
    def __init__(self, config_path: str):
        self.config = OmegaConf.load(config_path)

    @classmethod
    def from_built_in(cls, name: BuiltInCheckpointConfigName):
        path = os.path.join(os.path.dirname(__file__), "configs", name.value)
        return cls(config_path=path)

    def to_file_like(self):
        file_like = io.StringIO()
        OmegaConf.save(self.config, f=file_like)
        file_like.seek(0)
        return file_like

    def to_omegaconf(self) -> DictConfig:
        return self.config

    def to_version(self) -> SDVersion:
        if self.config.model.params.unet_config.params.context_dim == 768:
            return SDVersion.SD1x
        else:
            return SDVersion.SD2x



class StableDiffusionModel(SDType):
    def __init__(
        self, model: LatentDiffusion, version: SDVersion, device: Union[str, torch.device] = "cpu"
    ):
        self._model: LatentDiffusion = model
        self.to(device)
        self.version = version

    def to(self, device: Union[str, torch.device]) -> "StableDiffusionModel":
        """
        Modifies this object in-place.
        """
        torch_device = torch.device(device)
        if torch_device == self.device:
            return self

        self._model.to(torch_device)
        self.device = torch_device
        return self

    @classmethod
    def from_checkpoint(
        cls,
        checkpoint_filepath: str,
        config: Optional[CheckpointConfig] = None,
        device: Union[str, torch.device] = "cpu",
    ) -> "StableDiffusionModel":
        # CheckpointLoader
        sd, _, _ = load_checkpoint(checkpoint_filepath, config=config, device=device)
        return sd

    @SDType.requires_cuda
    def sample(
        self,
        positive: Conditioning,
        negative: Conditioning,
        latent_image: LatentImage,
        seed: int,
        steps: int,
        cfg_scale: float,
        sampler: Sampler,
        scheduler: Scheduler,
        denoise_strength: float,
    ) -> LatentImage:
        # KSampler

        img = common_ksampler(
            device=self.device,
            model=self._model,
            seed=seed,
            steps=steps,
            cfg=cfg_scale,
            sampler_name=sampler.value,
            scheduler=scheduler.value,
            positive=positive.to_internal_representation(),
            negative=negative.to_internal_representation(),
            latent=latent_image.to_internal_representation(),
            denoise=denoise_strength,
        )

        return LatentImage(img[0]["samples"], device=self.device)

    @SDType.requires_cuda
    def advanced_sample(
        self,
        positive: Conditioning,
        negative: Conditioning,
        latent_image: LatentImage,
        seed: int,
        steps: int,
        cfg_scale: float,
        sampler: Sampler,
        scheduler: Scheduler,
        denoise_strength: float,
        start_at_step: int,
        end_at_step: int,
        add_noise: bool,
        return_with_leftover_noise: bool,
    ) -> LatentImage:
        # KSamplerAdvanced

        force_full_denoise = True
        if return_with_leftover_noise == "enable":
            force_full_denoise = False
        disable_noise = False
        if add_noise == "disable":
            disable_noise = True

        img = common_ksampler(
            device=self.device,
            model=self._model,
            seed=seed,
            steps=steps,
            cfg=cfg_scale,
            sampler_name=sampler.value,
            scheduler=scheduler.value,
            positive=positive.to_internal_representation(),
            negative=negative.to_internal_representation(),
            latent=latent_image.to_internal_representation(),
            denoise=denoise_strength,
            force_full_denoise=force_full_denoise,
            disable_noise=disable_noise,
            start_step=start_at_step,
            last_step=end_at_step,
        )

        return LatentImage(img[0]["samples"], device=self.device)


def load_checkpoint(
    checkpoint_filepath: str,
    config: Optional[CheckpointConfig] = None,
    embedding_directory: Optional[str] = None,
    device: Union[str, torch.device] = "cpu",
) -> Tuple[StableDiffusionModel, CLIPModel, VAEModel]:

    # CheckpointLoader
    stable_diffusion_model_patcher: ModelPatcher
    try:
        if config is not None:
            stable_diffusion_model_patcher, clip, vae = _load_checkpoint(
                config_path=config.to_file_like() if config else None,
                ckpt_path=checkpoint_filepath,
                embedding_directory=embedding_directory,
            )
            version = config.to_version()
        else:

            stable_diffusion_model_patcher, clip, vae, version = _load_checkpoint_guess_config(
                ckpt_path=checkpoint_filepath,
                embedding_directory=embedding_directory,
            )
            if version == "SD1.x":
                version = SDVersion.SD1x
            else:
                version = SDVersion.SD2x
    except RuntimeError as e:
        raise ModelLoadError("Failed to load checkpoint.") from e

    return (
        StableDiffusionModel(stable_diffusion_model_patcher.model, device=device, version=version),
        CLIPModel(clip, device=device),
        VAEModel(vae, device=device),
    )
