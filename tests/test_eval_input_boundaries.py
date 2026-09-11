import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

import risk_service_api
from agent_safety_eval import run_eval


@pytest.mark.parametrize('kind', ['missing', 'empty_directory', 'no_paths'])
def test_no_scan_cannot_pass(tmp_path, kind):
    paths = [] if kind == 'no_paths' else [str(tmp_path / 'missing')]
    if kind == 'empty_directory':
        paths = [str(tmp_path)]
    result = run_eval(paths)
    assert result['passed'] is False
    assert result['errors']


def test_missing_input_is_not_hidden_by_clean_file(tmp_path):
    clean = tmp_path / 'clean.md'
    clean.write_text('A local demonstration.', encoding='utf-8')
    result = run_eval([str(clean), str(tmp_path / 'missing.md')])
    assert result['passed'] is False
    assert result['errors']


def test_api_rejects_outside_content_without_reading_it(tmp_path, monkeypatch):
    root = tmp_path / 'artifacts'
    root.mkdir()
    outside = tmp_path / 'outside.md'
    outside.write_text('private key SYNTHETIC_DO_NOT_RETURN', encoding='utf-8')
    monkeypatch.setattr(risk_service_api, 'EVAL_ROOT', root, raising=False)
    for requested in [str(outside), '../outside.md']:
        response = TestClient(risk_service_api.app).post('/eval', json={'files': [requested]})
        assert response.status_code == 200
        assert response.json()['passed'] is False
        assert response.json()['scanned_files'] == 0
        assert response.json()['errors']
        assert 'SYNTHETIC_DO_NOT_RETURN' not in response.text


def test_api_resolves_relative_input_under_fixed_root(tmp_path, monkeypatch):
    (tmp_path / 'clean.md').write_text('A local demonstration.', encoding='utf-8')
    monkeypatch.setattr(risk_service_api, 'EVAL_ROOT', tmp_path, raising=False)
    response = TestClient(risk_service_api.app).post('/eval', json={'files': ['clean.md']})
    assert response.json()['passed'] is True
    assert response.json()['scanned_files'] == 1


def test_symlink_cannot_escape_root(tmp_path):
    root = tmp_path / 'artifacts'
    root.mkdir()
    outside = tmp_path / 'outside.md'
    outside.write_text('private key SYNTHETIC_DO_NOT_RETURN', encoding='utf-8')
    try:
        (root / 'linked.md').symlink_to(outside)
    except OSError:
        pytest.skip('Creating symlinks requires OS permission')
    result = run_eval([str(root)], base_dir=root)
    assert result['passed'] is False
    assert 'SYNTHETIC_DO_NOT_RETURN' not in json.dumps(result)


def test_unreadable_input_is_a_structured_failure(tmp_path, monkeypatch):
    target = tmp_path / 'clean.md'
    target.write_text('A local demonstration.', encoding='utf-8')
    def denied(*args, **kwargs):
        raise PermissionError('synthetic read failure')
    monkeypatch.setattr(Path, 'read_text', denied)
    result = run_eval([str(target)])
    assert result['passed'] is False
    assert result['errors']


def test_langchain_tool_rejects_outside_file(tmp_path):
    from langchain_tool_caller import evaluate_artifact_safety
    outside = tmp_path / 'outside.md'
    outside.write_text('private key SYNTHETIC_DO_NOT_RETURN', encoding='utf-8')
    result = evaluate_artifact_safety.invoke({'paths': [str(outside)]})
    assert result['passed'] is False
    assert result['scanned_files'] == []
    assert 'SYNTHETIC_DO_NOT_RETURN' not in json.dumps(result)
