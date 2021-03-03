# REST API for News Summarization with Pegasus

## Install
1. Install packages
    > Note: Use python3.8 and update pip in virtual enviroment
    ```
    python3 -m venv env
    source env/bin/activate
    pip install -r requirements.txt
    ```
2. Create `server.json` for query (Only needed for **Usage 2.** and **3.**)
    ```
    (Under the root directory)
    vim server.json

    (Inside server.json)
    {
        "url": "your/server/url/for/query"
    }
    ```

## Usage
1. Deploy REST API
    ```
    python src/summarizer.py
    ```
2. Test the API\
    Run **1.** first, then:
    ```
    python test/test_summarizer.py
    ```
3. Test Pegasus
    ```
    python test/test_pegasus.py
    ```

## Citation
```bibtex
@misc{zhang2019pegasus,
    title={PEGASUS: Pre-training with Extracted Gap-sentences for Abstractive Summarization},
    author={Jingqing Zhang and Yao Zhao and Mohammad Saleh and Peter J. Liu},
    year={2019},
    eprint={1912.08777},
    archivePrefix={arXiv},
    primaryClass={cs.CL}
}
```