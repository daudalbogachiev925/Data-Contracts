from src.contract import DataContract
from src.validator import ContractValidator
from src.breaking import detect_breaking_changes
from src.versioning import bump_major, bump_minor
import pandas as pd

def test_validate_valid():
    c = DataContract.from_yaml("contracts/customers.yaml")
    df = pd.DataFrame({
        "customer_id": [1, 2, 3],
        "email": ["a@b.com", "c@d.com", "e@f.com"],
        "age": [25, 30, 40],
        "status": ["active", "inactive", "active"],
        "created_at": ["2024-01-01"] * 3,
    })
    assert ContractValidator(c).validate(df)["valid"] is True

def test_validate_invalid_enum():
    c = DataContract.from_yaml("contracts/customers.yaml")
    df = pd.DataFrame({
        "customer_id": [1], "email": ["a@b.com"],
        "status": ["unknown"], "created_at": ["2024-01-01"]})
    result = ContractValidator(c).validate(df)
    assert not result["valid"]

def test_version_bumps():
    assert bump_major("1.2.3") == "2.0.0"
    assert bump_minor("1.2.3") == "1.3.0"
