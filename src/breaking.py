from src.contract import DataContract

def detect_breaking_changes(old: DataContract, new: DataContract):
    changes = {"breaking": [], "non_breaking": []}

    old_fields = {f.name: f for f in old.fields}
    new_fields = {f.name: f for f in new.fields}

    removed = set(old_fields) - set(new_fields)
    added = set(new_fields) - set(old_fields)

    for r in removed:
        changes["breaking"].append({
            "type": "field_removed", "field": r,
            "reason": "Удалённое поле может использоваться downstream"})

    for a in added:
        f = new_fields[a]
        if f.required:
            changes["breaking"].append({
                "type": "required_field_added", "field": a,
                "reason": "Обязательное новое поле ломает producer"})
        else:
            changes["non_breaking"].append({
                "type": "optional_field_added", "field": a})

    for name, old_f in old_fields.items():
        if name not in new_fields:
            continue
        new_f = new_fields[name]
        if old_f.type != new_f.type:
            changes["breaking"].append({
                "type": "type_changed", "field": name,
                "old": old_f.type, "new": new_f.type})
        if old_f.required and not new_f.required:
            changes["non_breaking"].append({
                "type": "made_optional", "field": name})
        if not old_f.required and new_f.required:
            changes["breaking"].append({
                "type": "made_required", "field": name})
        if old_f.enum and new_f.enum and set(new_f.enum) < set(old_f.enum):
            changes["breaking"].append({
                "type": "enum_narrowed", "field": name,
                "removed": list(set(old_f.enum) - set(new_f.enum))})

    return changes
