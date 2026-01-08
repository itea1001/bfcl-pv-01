#!/bin/bash

# Run experiments for additional models: GPT-5 variants and reasoning models
# Models: gpt-5, gpt-5-mini, gpt-5-nano, o1-2024-12-17, o3-mini-2025-01-31

# Initialize conda
source /home/mingxuanl/miniconda3/etc/profile.d/conda.sh
conda activate BFCL1

# OPENAI_API_KEY should be set in environment before running this script

MODELS=("gpt-5-2025-08-07" "gpt-5-mini-2025-08-07" "gpt-5-nano-2025-08-07" "o1-2024-12-17" "o3-mini-2025-01-31")
CATEGORIES="simple,multiple,parallel,parallel_multiple,live_simple,live_multiple,live_parallel,live_parallel_multiple"  # 8 main prompting categories

# Define all 18 variations
RES_FMTS=("python" "python_tagged" "json" "json_tagged" "xml" "xml_tagged")
DOC_FMTS=("json" "python" "xml")

cd berkeley-function-call-leaderboard

for MODEL in "${MODELS[@]}"; do
    echo "=========================================="
    echo "Running model: $MODEL"
    echo "=========================================="
    
    for RES_FMT in "${RES_FMTS[@]}"; do
        for DOC_FMT in "${DOC_FMTS[@]}"; do
            VARIATION="res_fmt=${RES_FMT},doc_fmt=${DOC_FMT}"
            RESULT_DIR="result_${RES_FMT}_${DOC_FMT}"
            SCORE_DIR="score_${RES_FMT}_${DOC_FMT}"
            
            echo "Running: $MODEL - $VARIATION"
            
            # Generate
            python -m bfcl generate \
                --model "$MODEL" \
                --test-category "$CATEGORIES" \
                --prompt-variation "$VARIATION" \
                --result-dir "$RESULT_DIR" \
                --num-threads 32
            
            if [ $? -ne 0 ]; then
                echo "ERROR: Generation failed for $MODEL - $VARIATION"
                continue
            fi
            
            # Evaluate
            python -m bfcl evaluate \
                --model "$MODEL" \
                --test-category "$CATEGORIES" \
                --prompt-variation "$VARIATION" \
                --result-dir "$RESULT_DIR" \
                --score-dir "$SCORE_DIR"
            
            if [ $? -ne 0 ]; then
                echo "ERROR: Evaluation failed for $MODEL - $VARIATION"
            fi
            
            echo "Completed: $MODEL - $VARIATION"
            echo "------------------------------------------"
        done
    done
done

echo "=========================================="
echo "All experiments completed!"
echo "=========================================="

