import json

def get_gemini_extract_data_prompt(markdown_cv: str):
    return f"""
        Eres un extractor de información para career coaching.

        Tu tarea es analizar el siguiente CV en formato markdown y devolver ÚNICAMENTE
        un JSON válido que cumpla exactamente con el schema proporcionado.

        Reglas:
        - No inventes información.
        - Si un dato no aparece, devuelve string vacío, arreglo vacío o null cuando aplique.
        - Normaliza skills técnicas y tecnologías.
        - Resume el perfil profesional en un campo "summary".
        - Infiere "target_roles_inferred" basándote en experiencia, proyectos y skills.
        - No devuelvas markdown.
        - No devuelvas explicación.
        - Solo JSON válido.

        CV en markdown:
        {markdown_cv}
    """

SCHEMA_EXTRACT_DATA = {
        "type": "object",
        "properties": {
            "full_name": {"type": "string"},
            "email": {"type": "string"},
            "phone": {"type": "string"},
            "location": {"type": "string"},
            "linkedin": {"type": "string"},
            "github": {"type": "string"},
            "portfolio": {"type": "string"},
            "summary": {"type": "string"},
            "years_of_experience": {"type": "number"},
            "education": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "institution": {"type": "string"},
                        "degree": {"type": "string"},
                        "field_of_study": {"type": "string"},
                        "start_date": {"type": "string"},
                        "end_date": {"type": "string"}
                    },
                    "required": ["institution", "degree"]
                }
            },
            "work_experience": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "company": {"type": "string"},
                        "role": {"type": "string"},
                        "start_date": {"type": "string"},
                        "end_date": {"type": "string"},
                        "responsibilities": {
                            "type": "array",
                            "items": {"type": "string"}
                        },
                        "technologies": {
                            "type": "array",
                            "items": {"type": "string"}
                        }
                    },
                    "required": ["company", "role"]
                }
            },
            "skills": {
                "type": "object",
                "properties": {
                    "technical": {
                        "type": "array",
                        "items": {"type": "string"}
                    },
                    "tools": {
                        "type": "array",
                        "items": {"type": "string"}
                    },
                    "soft": {
                        "type": "array",
                        "items": {"type": "string"}
                    },
                    "languages": {
                        "type": "array",
                        "items": {"type": "string"}
                    }
                }
            },
            "certifications": {
                "type": "array",
                "items": {"type": "string"}
            },
            "projects": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "description": {"type": "string"},
                        "technologies": {
                            "type": "array",
                            "items": {"type": "string"}
                        }
                    },
                    "required": ["name"]
                }
            },
            "target_roles_inferred": {
                "type": "array",
                "items": {"type": "string"}
            }
        },
        "required": [
            "full_name",
            "summary",
            "skills",
            "work_experience",
            "education",
            "projects",
            "target_roles_inferred"
        ]
    }

def get_gemini_career_path_prompt(cv_data: str):
    return f"""
        Eres un career coach técnico especializado en tecnología.

        Con base en el siguiente JSON extraído de un CV, genera un career path personalizado.

        Objetivo:
        - Recomendar exactamente 3 rutas profesionales viables.
        - Todas las rutas y su información debe estar en inglés.
        - Ordenarlas de mayor a menor compatibilidad.
        - Pensar como un asesor realista: no inventar experiencia que no existe.
        - Basarte en skills, experiencia, proyectos, educación y seniority aproximado.

        Reglas:
        - Devuelve SOLO JSON válido.
        - No devuelvas markdown.
        - No devuelvas explicación fuera del JSON.
        - "match_score" debe ser un número de 0 a 100.
        - "path_id" debe ser un slug corto en snake_case.
        - "suggested_projects" debe incluir proyectos realistas para fortalecer empleabilidad.
        - "roadmap" debe venir por fases progresivas.
        - "next_30_days_plan" debe ser accionable.
        - Los paths deben ser concretos, por ejemplo:
        - backend_engineer
        - frontend_engineer
        - fullstack_engineer
        - devops_engineer
        - data_analyst
        - ml_engineer
        - qa_automation_engineer
        - cloud_engineer
        - salesforce_developer
        - mobile_developer
        - Si el perfil es junior, el roadmap debe reflejar crecimiento junior -> mid.
        - Evita recomendaciones absurdas o demasiado lejanas al perfil.

        CV_DATA:
        {json.dumps(cv_data, ensure_ascii=False, indent=2)}
    """

SCHEMA_CAREER_PATH = {
        "type": "object",
        "properties": {
            "profile_summary": {
                "type": "object",
                "properties": {
                    "current_level": {"type": "string"},
                    "estimated_experience_years": {"type": "number"},
                    "main_strengths": {
                        "type": "array",
                        "items": {"type": "string"}
                    },
                    "top_skill_gaps": {
                        "type": "array",
                        "items": {"type": "string"}
                    },
                    "recommended_primary_path": {"type": "string"}
                },
                "required": [
                    "current_level",
                    "estimated_experience_years",
                    "main_strengths",
                    "top_skill_gaps",
                    "recommended_primary_path"
                ]
            },
            "recommended_paths": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "path_id": {"type": "string"},
                        "title": {"type": "string"},
                        "match_score": {"type": "number"},
                        "why_this_path": {"type": "string"},
                        "candidate_fit_summary": {"type": "string"},
                        "current_strengths": {
                            "type": "array",
                            "items": {"type": "string"}
                        },
                        "skill_gaps": {
                            "type": "array",
                            "items": {"type": "string"}
                        },
                        "recommended_learning_topics": {
                            "type": "array",
                            "items": {"type": "string"}
                        },
                        "suggested_projects": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "title": {"type": "string"},
                                    "description": {"type": "string"},
                                    "difficulty": {"type": "string"},
                                    "estimated_weeks": {"type": "number"},
                                    "skills_validated": {
                                        "type": "array",
                                        "items": {"type": "string"}
                                    }
                                },
                                "required": [
                                    "title",
                                    "description",
                                    "difficulty",
                                    "estimated_weeks",
                                    "skills_validated"
                                ]
                            }
                        },
                        "roadmap": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "phase": {"type": "string"},
                                    "duration": {"type": "string"},
                                    "goal": {"type": "string"},
                                    "milestones": {
                                        "type": "array",
                                        "items": {"type": "string"}
                                    }
                                },
                                "required": ["phase", "duration", "goal", "milestones"]
                            }
                        },
                        "recommended_certifications": {
                            "type": "array",
                            "items": {"type": "string"}
                        },
                        "target_roles": {
                            "type": "array",
                            "items": {"type": "string"}
                        },
                        "next_30_days_plan": {
                            "type": "array",
                            "items": {"type": "string"}
                        }
                    },
                    "required": [
                        "path_id",
                        "title",
                        "match_score",
                        "why_this_path",
                        "candidate_fit_summary",
                        "current_strengths",
                        "skill_gaps",
                        "recommended_learning_topics",
                        "suggested_projects",
                        "roadmap",
                        "recommended_certifications",
                        "target_roles",
                        "next_30_days_plan"
                    ]
                }
            }
        },
        "required": ["profile_summary", "recommended_paths"]
    }