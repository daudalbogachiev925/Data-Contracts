import pandas as pd
from src.contract import DataContract

class ContractValidator:
    def __init__(self, contract: DataContract):
        self.contract = contract

    def validate(self, df: pd.DataFrame):
        errors = []
        warnings = []

        schema_fields = {f.name for f in self.contract.fields}
        df_fields = set(df.columns)

        missing = schema_fields - df_fields
        extra = df_fields - schema_fields
        if missing:
            errors.append(f"Missing fields: {missing}")
        if extra:
            warnings.append(f"Extra fields (not in contract): {extra}")

        for field in self.contract.fields:
            if field.name not in df.columns:
                continue
            series = df[field.name]
            if field.required and series.isnull().any():
                errors.append(f"{field.name}: null values in required field")
            if field.enum:
                invalid = set(series.dropna().unique()) - set(field.enum)
                if invalid:
                    errors.append(f"{field.name}: invalid enum values {invalid}")
            if field.min_value is not None:
                try:
                    if (series.dropna().astype(float) < field.min_value).any():
                        errors.append(f"{field.name}: values below min {field.min_value}")
                except (ValueError, TypeError):
                    pass
            if field.max_value is not None:
                try:
                    if (series.dropna().astype(float) > field.max_value).any():
                        errors.append(f"{field.name}: values above max {field.max_value}")
                except (ValueError, TypeError):
                    pass

        return {"valid": len(errors) == 0, "errors": errors, "warnings": warnings}
