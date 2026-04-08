import logging
from typing import cast
from litellm import acompletion, ModelResponse
from vllm.engine.arg_utils import AsyncEngineArgs
from vllm.engine.async_llm_engine import AsyncLLMEngine

logger = logging.getLogger(__name__)

# Cloud Model Configuration (LiteLLM)
CLOUD_MODEL_NAME = "gemini/gemini-flash-lite-latest"

async def generate_cloud_response(system_prompt: str, user_prompt: str) -> str:
    """
    Calls the Google Gemini API asynchronously via LiteLLM.
    """
    try:
        raw_response = await acompletion(
            model=CLOUD_MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=1.0,
            max_tokens=150
        )

        response = cast(ModelResponse, raw_response)

        return response.choices[0].message.content or ""
    except Exception as e:
        logger.error(f"Cloud LLM failure: {e}")
        return "I am currently unable to process your request."

# Local Model Configuration (vLLM)
LOCAL_MODEL_NAME = "casperhansen/llama-3-8b-instruct-awq"

def init_vllm_engine() -> AsyncLLMEngine:
    """
    Initializes the local vLLM engine.
    This allocates VRAM immediately upon startup.
    """
    logger.info(f"Initializing vLLM with model {LOCAL_MODEL_NAME}...")
    
    # gpu_memory_utilization=0.8 means vLLM will reserve strictly 80% of the VRAM
    # preventing CUDA OOM crashes and leaving some VRAM for the OS/Docker
    engine_args = AsyncEngineArgs(
        model=LOCAL_MODEL_NAME,
        quantization="awq",
        tensor_parallel_size=1,
        gpu_memory_utilization=0.8,
        max_model_len=2048, # Restrict max context to save VRAM
        enforce_eager=True  # Can help with memory fragmentation on smaller GPUs
    )
    
    return AsyncLLMEngine.from_engine_args(engine_args)

# We will instantiate this engine later in the application lifecycle
vllm_engine = None