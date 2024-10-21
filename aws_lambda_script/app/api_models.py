# ns_models.py
from flask_restx import fields

def get_project_model():
    from .resources import ns

    # Define all models globally
    user_model = ns.model('User', {
        'email': fields.String(required=True, description="User email"),
        'roles': fields.List(fields.String, required=True, description="Roles of the user")
    })

    architecture_model = ns.model('Architecture', {
        'hosting': fields.Nested(ns.model('Hosting', {
            'type': fields.String(required=True, description="Type of hosting"),
            'detail': fields.List(fields.String, required=False, description="Details of hosting")
        })),
        'database': fields.Nested(ns.model('Database', {
            'main': fields.String(required=True, description="Main database"),
            'others': fields.List(fields.String, required=False, description="Other databases")
        })),
        'languages': fields.Nested(ns.model('Languages', {
            'main': fields.String(required=True, description="Main language"),
            'others': fields.List(fields.String, required=False, description="Other languages")
        })),
        'frameworks': fields.Nested(ns.model('Frameworks', {
            'main': fields.String(required=True, description="Main framework"),
            'others': fields.List(fields.String, required=False, description="Other frameworks")
        })),
        'CICD': fields.Nested(ns.model('CICD', {
            'main': fields.String(required=True, description="Main CICD tool"),
            'others': fields.List(fields.String, required=False, description="Other CICD tools")
        })),
        'infrastructure': fields.Nested(ns.model('Infrastructure', {
            'main': fields.String(required=True, description="Main infrastructure tool"),
            'others': fields.List(fields.String, required=False, description="Other infrastructure tools")
        }))
    })

    details_model = ns.model('Details', {
            'name': fields.String(required=True, description="Project name"),
            'short_name': fields.String(required=True, description="Short name of the project"),
            'documentation_link': fields.String(required=False, description="Link to the project documentation"),
            'project_description': fields.String(required=True, description="Description of the project"),
     })

    # Project Model
    project_model = ns.model('Project', {
        'user': fields.List(fields.Nested(user_model), required=True, description="List of users"),
        'details': fields.List(fields.Nested(details_model), required=True, description="Details of project"),
        'developed': fields.List(fields.Raw, required=True, description="Development details"),
        'source_control': fields.List(fields.String, required=True, description="Source control platforms"),
        'architecture': fields.Nested(architecture_model, required=True, description="Architecture details"),
        'archived': fields.Boolean(required=True, description="Archived status of the project")
    })

    return project_model

def get_new_project_model():
    from .resources import ns

    user_model = ns.model('User', {
        'email': fields.String(required=True, description="User email"),
        'roles': fields.List(fields.String, required=True, description="Roles of the user"),
        'grade': fields.String(required=False, description="Grade of the user")
    })

    details_model = ns.model('Details', {
        'name': fields.String(required=True, description="Project name"),
        'short_name': fields.String(required=True, description="Short name of the project"),
        'documentation_link': fields.List(fields.String, required=False, description="Link to the project documentation"),
        'project_description': fields.String(required=False, description="Description of the project")
    })

    source_control_model = ns.model('SourceControl', {
        'type': fields.String(required=True, description="Type of source control"),
        'links': fields.List(fields.Nested(ns.model('RepoLink', {
            'repo_link_1': fields.String(required=False, description="Repository link 1"),
            'repo_link_2': fields.String(required=False, description="Repository link 2")
        })), required=True, description="Links to repositories")
    })

    architecture_model = ns.model('Architecture', {
        'hosting': fields.Nested(ns.model('Hosting', {
            'type': fields.String(required=True, description="Type of hosting"),
            'detail': fields.List(fields.String, required=False, description="Details of hosting")
        })),
        'database': fields.Nested(ns.model('Database', {
            'main': fields.List(fields.String, required=True, description="Main database"),
            'others': fields.List(fields.String, required=False, description="Other databases")
        })),
        'languages': fields.Nested(ns.model('Languages', {
            'main': fields.List(fields.String, required=True, description="Main language"),
            'others': fields.List(fields.String, required=False, description="Other languages")
        })),
        'frameworks': fields.Nested(ns.model('Frameworks', {
            'main': fields.List(fields.String, required=True, description="Main framework"),
            'others': fields.List(fields.String, required=False, description="Other frameworks")
        })),
        'CICD': fields.Nested(ns.model('CICD', {
            'main': fields.List(fields.String, required=True, description="Main CICD tool"),
            'others': fields.List(fields.String, required=False, description="Other CICD tools")
        })),
        'infrastructure': fields.Nested(ns.model('Infrastructure', {
            'main': fields.List(fields.String, required=True, description="Main infrastructure tool"),
            'others': fields.List(fields.String, required=False, description="Other infrastructure tools")
        }))
    })

    project_model = ns.model('Project', {
        'user': fields.List(fields.Nested(user_model), required=True, description="List of users"),
        'details': fields.List(fields.Nested(details_model), required=True, description="Details of project"),
        'developed': fields.List(fields.Raw, required=True, description="Development details"),
        'source_control': fields.List(fields.Nested(source_control_model), required=True, description="Source control platforms"),
        'architecture': fields.Nested(architecture_model, required=True, description="Architecture details"),
        'archived': fields.Boolean(required=True, description="Archived status of the project")
    })

    return project_model
