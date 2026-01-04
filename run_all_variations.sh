#!/bin/bash
# Run all prompt variation combinations for multiple models and categories

set -e  # Exit on error

# Configuration
MODELS=("gpt-4o-mini-2024-07-18" "gpt-4o-2024-11-20" "gpt-4.1-2025-04-14")
RESPONSE_FORMATS=("python" "python_tagged" "json" "json_tagged" "xml" "xml_tagged")
DOC_FORMATS=("json" "python" "xml")
CATEGORIES=("all")  # Will run all 8 categories

# OPENAI_API_KEY should be set in environment before running this script

cd berkeley-function-call-leaderboard

echo "Starting full evaluation: ${#MODELS[@]} models × ${#RESPONSE_FORMATS[@]} response formats × ${#DOC_FORMATS[@]} doc formats × ${#CATEGORIES[@]} category groups"
echo "Total: $((${#MODELS[@]} * ${#RESPONSE_FORMATS[@]} * ${#DOC_FORMATS[@]} * ${#CATEGORIES[@]})) combinations"
echo ""

for MODEL in "${MODELS[@]}"; do
    echo "=== Model: $MODEL ==="
    
    for RES_FMT in "${RESPONSE_FORMATS[@]}"; do
        for DOC_FMT in "${DOC_FORMATS[@]}"; do
            VARIATION="res_fmt=${RES_FMT},doc_fmt=${DOC_FMT}"
            RESULT_DIR="result_${RES_FMT}_${DOC_FMT}"
            SCORE_DIR="score_${RES_FMT}_${DOC_FMT}"
            
            echo "Running: ${VARIATION}"
            
            # Generate
            python -m bfcl generate \
                --model "$MODEL" \
                --test-category all \
                --prompt-variation "$VARIATION" \
                --result-dir "$RESULT_DIR" \
                --num-threads 16 \
                --allow-overwrite
            
            # Evaluate
            python -m bfcl evaluate \
                --model "$MODEL" \
                --test-category all \
                --prompt-variation "$VARIATION" \
                --result-dir "$RESULT_DIR" \
                --score-dir "$SCORE_DIR"
            
            echo "✓ Completed: ${MODEL} - ${VARIATION}"
            echo ""
        done
    done
    
    echo "✓✓✓ Completed all variations for $MODEL"
    echo ""
done

echo "All evaluations complete!"

