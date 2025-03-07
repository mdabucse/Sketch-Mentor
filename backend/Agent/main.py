import logging
from VisualAgent.config import Config
from VisualAgent.pipeline import AgenticPipeline

def main():
    """Entry point for the agentic visualization code generator."""
    # Setup logging
    logger = Config.setup_logging()
    logger.info("Starting the agentic visualization system.")
    
    # Initialize clients
    # gemini_model, openrouter_client = Config.initialize_clients()
    
    # Create the pipeline
    gemini_flash_model, gemini_learn_model, openrouter_client = Config.initialize_clients()
    qwen_model = Config.QWEN_MODEL
    logger.info("API clients initialized successfully.")

    # Create pipeline
    pipeline = AgenticPipeline(gemini_flash_model, gemini_learn_model, openrouter_client, qwen_model)
    logger.info("Agentic pipeline created.")
    
    # Example usage
    user_prompt = input("Enter a mathematical concept to visualize: ")
    logger.info(f"Processing user prompt: {user_prompt}")
    
    try:
        generated_code = pipeline.run(user_prompt)
        logger.info("Code generation completed.")
        
        print("\nGenerated p5.js Code:")
        print("=====================")
        print(generated_code)
        
        # Save the generated code to a file
        with open("generated_visualization.js", "w") as f:
            f.write(generated_code)
        logger.info("Code saved to 'generated_visualization.js'")
        print("\nCode saved to 'generated_visualization.js'")
        
    except Exception as e:
        logger.error(f"Error in main execution: {str(e)}")
        print(f"Error: {str(e)}")

    logger.info("Execution completed.")

if __name__ == "__main__":
    main()