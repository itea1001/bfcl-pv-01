#!/bin/bash

# Run experiments for xAI Grok models
# Models: grok-4-0709, grok-3-beta, grok-3-mini-beta

# Initialize conda
source /home/mingxuanl/miniconda3/etc/profile.d/conda.sh
conda activate BFCL1

# Navigate to the leaderboard directory
cd /home/mingxuanl/mingxuanl/simulation/brandonzhang/bfcl-pv-01/berkeley-function-call-leaderboard

# Set Grok API key (should be set in environment before running this script)
# export GROK_API_KEY=your_grok_api_key_here

# Define models, response formats, doc formats, and test categories
MODELS=("grok-4-0709" "grok-3-beta" "grok-3-mini-beta")
RES_FMTS=("python" "python_tagged" "json" "json_tagged" "xml" "xml_tagged")
DOC_FMTS=("json" "python" "xml")
CATEGORIES="simple,multiple,parallel,parallel_multiple,live_simple,live_multiple,live_parallel,live_parallel_multiple"

# Loop through each model
for MODEL in "${MODELS[@]}"; do
    echo "=========================================="
    echo "Running model: $MODEL"
    echo "=========================================="
    
    # Loop through each response format
    for RES_FMT in "${RES_FMTS[@]}"; do
        # Loop through each doc format
        for DOC_FMT in "${DOC_FMTS[@]}"; do
            PROMPT_VARIATION="res_fmt=${RES_FMT},doc_fmt=${DOC_FMT}"
            RESULT_DIR="result_${RES_FMT}_${DOC_FMT}"
            SCORE_DIR="score_${RES_FMT}_${DOC_FMT}"

            echo "Running: $MODEL - $PROMPT_VARIATION"

            # Generate LLM responses
            python -m bfcl generate \
                --model "$MODEL" \
                --test-category "$CATEGORIES" \
                --prompt-variation "$PROMPT_VARIATION" \
                --result-dir "$RESULT_DIR" \
                --num-threads 32 \
                --allow-overwrite

            if [ $? -ne 0 ]; then
                echo "ERROR: Generation failed for $MODEL - $PROMPT_VARIATION"
                continue
            fi

            # Evaluate the generated responses
            python -m bfcl evaluate \
                --model "$MODEL" \
                --test-category "$CATEGORIES" \
                --prompt-variation "$PROMPT_VARIATION" \
                --result-dir "$RESULT_DIR" \
                --score-dir "$SCORE_DIR"

            if [ $? -ne 0 ]; then
                echo "ERROR: Evaluation failed for $MODEL - $PROMPT_VARIATION"
            fi

            echo "Completed: $MODEL - $PROMPT_VARIATION"
            echo "------------------------------------------"
        done
    done
done

echo "=========================================="
echo "All Grok experiments completed!"
echo "=========================================="

