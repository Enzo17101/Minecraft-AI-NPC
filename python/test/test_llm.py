import asyncio
import logging
from dotenv import load_dotenv
from vllm.sampling_params import SamplingParams
from src.core.ai_engine import generate_cloud_response, init_vllm_engine

import time

# Load .env variables (MODEL_API_KEY, HF_TOKEN)
load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def run_tests():
    logger.info("--- Starting AI Engines Test ---")

    for i in range(3):

        # Test Cloud Engine (Cloud Model)
        logger.info("Testing Cloud Model...")

        start = time.time()

        cloud_result = await generate_cloud_response(
            system_prompt="You are a helpful assistant.",
            user_prompt=f"Say 'Banana {i} !' and nothing else."
        )
        end = time.time()
        print("gemini response time : ", end - start)
        logger.info(f"Cloud Response: {cloud_result.strip()}")

    # Test Local Engine (vLLM + Llama 3 AWQ)
    logger.info("Testing Local Model (vLLM)... (This will download ~5GB if first time)")
    try:
        start_init = time.time()

        engine = init_vllm_engine()
        end_init = time.time()
        print("init vllm engeine time : ", end_init - start_init)
        
        
        prompt = "<|begin_of_text|><|start_header_id|>user<|end_header_id|>\n\nSay the word 'Apple' and nothing else.<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n"
        
        sampling_params = SamplingParams(temperature=0.0, max_tokens=10)
        
        # AsyncGenerator iteration pattern required by vLLM
        request_id = "test_req_1"
        final_output = ""

        start = time.time()

        async for request_output in engine.generate(prompt, sampling_params, request_id):
            final_output = request_output.outputs[0].text
        end = time.time()
        print("vllm response time : ", end - start)

        logger.info(f"Local Response: {final_output.strip()}")
        
    except Exception as e:
        logger.error(f"Local LLM failure: {e}")

if __name__ == "__main__":
    asyncio.run(run_tests())