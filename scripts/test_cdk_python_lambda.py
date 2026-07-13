#!/usr/bin/env python3
import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LAMBDA_DIR = ROOT / "cdk_python_lambda"


def read(relative_path: str) -> str:
    return (LAMBDA_DIR / relative_path).read_text(encoding="utf-8")


def test_dockerfile_uses_lambda_al2023_python_image() -> None:
    dockerfile = read("deploy/Dockerfile")

    assert "FROM public.ecr.aws/lambda/python:3.14" in dockerfile
    assert "ubuntu:" not in dockerfile
    assert "apt-get" not in dockerfile
    assert "python3.6" not in dockerfile
    assert "node-v10" not in dockerfile
    assert "TO" + "DO" not in dockerfile


def test_dockerfile_uses_current_node_lts_for_cdk() -> None:
    dockerfile = read("deploy/Dockerfile")

    assert "ARG NODE_VERSION=24.18.0" in dockerfile
    assert "node-v${NODE_VERSION}" in dockerfile
    assert "aws-cdk@latest" in dockerfile


def test_cdk_code_uses_v2_and_current_lambda_runtime() -> None:
    requirements = read("deploy/requirements.txt")
    app = read("deploy/app.py")
    stack = read("deploy/my_stack.py")

    assert "aws-cdk-lib" in requirements
    assert "constructs" in requirements
    assert "aws-cdk.core" not in requirements
    assert "from aws_cdk import core" not in app
    assert "from aws_cdk import core" not in stack
    assert "Runtime.PYTHON_3_14" in stack


def test_application_dependencies_are_current_enough() -> None:
    requirements = read("source/requirements.txt")

    assert "requests==2.34.2" in requirements
    assert "boto3==1.43.46" in requirements
    assert "urllib3==2.7.0" in requirements


def test_python_sources_parse() -> None:
    for relative_path in [
        "deploy/app.py",
        "deploy/my_stack.py",
        "source/main.py",
    ]:
        ast.parse(read(relative_path), filename=relative_path)


def run() -> None:
    tests = [
        test_dockerfile_uses_lambda_al2023_python_image,
        test_dockerfile_uses_current_node_lts_for_cdk,
        test_cdk_code_uses_v2_and_current_lambda_runtime,
        test_application_dependencies_are_current_enough,
        test_python_sources_parse,
    ]
    for test in tests:
        test()


if __name__ == "__main__":
    run()
