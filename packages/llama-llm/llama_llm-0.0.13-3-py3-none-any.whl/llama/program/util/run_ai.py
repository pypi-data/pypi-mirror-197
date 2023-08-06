
import requests
import os
from llama.program.util.config import get_config, edit_config
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import tenacity


def query_run_program(params):
    key, url = get_url_and_key()
    resp = powerml_run_program(params, url, key)
    return resp


@tenacity.retry(stop=tenacity.stop_after_attempt(3))
def powerml_run_program(params, url, key):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + key,
    }
    response = requests.post(
        url=url + "/v1/run_llama_program",
        headers=headers,
        json=params)
    if response.status_code != 200:
        try:
            description = response.json()
        except BaseException:
            description = response.status_code
        finally:
            print(f"API error {description}. Retrying...")
            raise Exception(f"API error {description}")
    return response


def query_run_embedding(prompt, config={}):
    params = {
        'prompt': prompt
    }
    edit_config(config)
    key, url = get_url_and_key()
    resp = powerml_run_embedding(params, url, key)
    return np.reshape(resp.json()['embedding'], (1, -1))


def fuzzy_is_duplicate(embedding, reference_embeddings, threshold=0.99):
    if embedding is None:
        return True
    if not reference_embeddings:
        return False
    similarities = [
        cosine_similarity(embedding, reference_embedding)
        for reference_embedding in reference_embeddings
    ]

    most_similar_index = np.argmax(similarities)

    return similarities[most_similar_index] > threshold


def powerml_run_embedding(params, url, key):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + key,
    }
    response = requests.post(
        url=url + "/v1/embedding",
        headers=headers,
        json=params)
    if response.status_code != 200:
        try:
            description = response.json()
            print(description)
        except BaseException:
            description = response.status_code
        finally:
            raise Exception(f"API error {description}")
    return response


def get_url_and_key():
    cfg = get_config()
    environment = os.environ.get("LLAMA_ENVIRONMENT")
    if environment == "LOCAL":
        key = 'test_token'
        if 'local' in cfg:
            if 'key' in cfg["local"]:
                key = cfg['local.key']
        url = "http://localhost:5001"
    elif environment == "STAGING":
        key = cfg['staging.key']
        url = 'https://api.staging.powerml.co'
    else:
        key = cfg['production.key']
        url = 'https://api.powerml.co'
    return (key, url)
