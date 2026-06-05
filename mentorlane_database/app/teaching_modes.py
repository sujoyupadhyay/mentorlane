from __future__ import annotations
from flask import Blueprint, abort, request
from .database import mysql_session

teaching_mode_bp = Blueprint("teaching_mode_api", __name__, url_prefix="/api/teaching-modes")

@teaching_mode_bp.route("", methods=["POST"])
def create_teaching_mode() -> tuple[dict[str, object], int]:
    """Create a teaching mode entry.

    ---
    tags:
      - Teaching Modes
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              teaching_mode:
                type: string
                example: In-person
              description:
                type: string
                example: Face to face mentoring
            required:
              - teaching_mode
    responses:
      201:
        description: Teaching mode created successfully
      400:
        description: Invalid payload
    """

    payload = request.get_json(silent=True) or {}
    teaching_mode = payload.get("teaching_mode")
    description = payload.get("description")

    if not teaching_mode:
        abort(400, "Payload must include 'teaching_mode'.")

    with mysql_session() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO teaching_modes (teaching_mode, description) VALUES (%s, %s)",
                (teaching_mode, description),
            )
            new_id = cursor.lastrowid

    return {
        "teaching_mode_id": new_id,
        "teaching_mode": teaching_mode,
        "description": description,
    }, 201
