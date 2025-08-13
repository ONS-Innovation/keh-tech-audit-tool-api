from flask_restx import fields


# Had problems with initialising this as 'ns' wouldn't have been initialised so it would fail.
# Making this a function would the model to intialised when it's used and when 'ns' has been initialised.
def get_project_model():
    from .resources import ns

    user_model = ns.model(
        "User",
        {
            "email": fields.String(required=True, description="User email"),
            "roles": fields.List(
                fields.String, required=False, description="Roles of the user"
            ),
            "grade": fields.String(required=False, description="Grade of the user"),
        },
    )

    details_model = ns.model(
        "Details",
        {
            "programme_name": fields.String(
                required=False, description="Programme name", default="N/A"
            ),
            "programme_short_name": fields.String(
                required=False, description="Programme short name", default="N/A"
            ),
            "name": fields.String(required=True, description="Project name"),
            "short_name": fields.String(
                required=False, description="Short name of the project"
            ),
            "documentation_link": fields.List(
                fields.String,
                required=False,
                description="Link to the project documentation",
            ),
            "project_description": fields.String(
                required=False, description="Description of the project"
            ),
            "project_dependencies": fields.List(
                fields.Nested(
                    ns.model(
                        "project_dependency",
                        {
                            "name": fields.String(
                                required=False,
                                description="Name of the project",
                            ),
                            "description": fields.String(
                                required=False,
                                description="Description of the dependency",
                            ),
                        },
                    )
                ),
                required=False,
                description="A List of project dependencies",
            ),
        },
    )

    source_control_model = ns.model(
        "SourceControl",
        {
            "type": fields.String(required=False, description="Type of source control"),
            "links": fields.List(
                fields.Nested(
                    ns.model(
                        "RepoLink",
                        {
                            "description": fields.String(
                                required=False,
                                description="Description of the repository link",
                            ),
                            "url": fields.String(
                                required=False, description="URL of the repository link"
                            ),
                        },
                    )
                ),
                required=False,
                description="Links to repositories",
            ),
        },
    )

    architecture_model = ns.model(
        "Architecture",
        {
            "hosting": fields.Nested(
                ns.model(
                    "Hosting",
                    {
                        "type": fields.List(
                            fields.String, required=False, description="Type of hosting"
                        ),
                        "details": fields.List(
                            fields.String,
                            required=False,
                            description="Other hosting types",
                        ),
                    },
                )
            ),
            "database": fields.Nested(
                ns.model(
                    "Database",
                    {
                        "main": fields.List(
                            fields.String, required=False, description="Main database"
                        ),
                        "others": fields.List(
                            fields.String, required=False, description="Other databases"
                        ),
                    },
                )
            ),
            "languages": fields.Nested(
                ns.model(
                    "Languages",
                    {
                        "main": fields.List(
                            fields.String, required=False, description="Main language"
                        ),
                        "others": fields.List(
                            fields.String, required=False, description="Other languages"
                        ),
                    },
                )
            ),
            "frameworks": fields.Nested(
                ns.model(
                    "Frameworks",
                    {
                        "main": fields.List(
                            fields.String, required=False, description="Main framework"
                        ),
                        "others": fields.List(
                            fields.String,
                            required=True,
                            description="Other frameworks",
                        ),
                    },
                )
            ),
            "cicd": fields.Nested(
                ns.model(
                    "cicd",
                    {
                        "main": fields.List(
                            fields.String, required=False, description="Main CICD tool"
                        ),
                        "others": fields.List(
                            fields.String,
                            required=True,
                            description="Other CICD tools",
                        ),
                    },
                )
            ),
            "environments": fields.Nested(
                ns.model(
                    "environments",
                    {
                        "dev": fields.Boolean(required=False, description="Development environment status"),
                        "int": fields.Boolean(required=False, description="Integration environment status"),        
                        "uat": fields.Boolean(required=False, description="User Acceptance Testing environment status"),
                        "preprod": fields.Boolean(required=False, description="Pre-production or staging environment status"),
                        "prod": fields.Boolean(required=False, description="Production environment status"),
                        "postprod": fields.Boolean(required=False, description="Post-production environment status")
                    }
                )
            ),
            "infrastructure": fields.Nested(
                ns.model(
                    "Infrastructure",
                    {
                        "main": fields.List(
                            fields.String,
                            required=False,
                            description="Main infrastructure tool",
                        ),
                        "others": fields.List(
                            fields.String,
                            required=False,
                            description="Other infrastructure tools",
                        ),
                    },
                )
            ),
            "publishing": fields.Nested(
                ns.model(
                    "publishing",
                    {
                        "main": fields.List(
                            fields.String,
                            required=False,
                            description="Main targets are internal publishing targets e.g. Github Release/ Tags, Amazon ECR Private Gallery",
                        ),
                        "others": fields.List(
                            fields.String,
                            required=False,
                            description="Other targets are external publishing target e.g. Artifactory, PyPi, CRAN, Amazon ECR Public Gallery",
                        ),
                    },
                )
            ),
        },
    )

    supporting_tools_model = ns.model(
        "SupportingTools",
        {
            "code_editors": fields.Nested(
                ns.model(
                    "code_editors",
                    {
                        "main": fields.List(
                            fields.String,
                            required=False,
                            description="Main code editor",
                        ),
                        "others": fields.List(
                            fields.String,
                            required=False,
                            description="Other code editors",
                        ),
                    },
                )
            ),
            "user_interface": fields.Nested(
                ns.model(
                    "user_interface",
                    {
                        "main": fields.List(
                            fields.String, required=False, description="Main UI tool"
                        ),
                        "others": fields.List(
                            fields.String, required=False, description="Other UI tools"
                        ),
                    },
                )
            ),
            "diagrams": fields.Nested(
                ns.model(
                    "diagrams",
                    {
                        "main": fields.List(
                            fields.String,
                            required=False,
                            description="Main diagram tool",
                        ),
                        "others": fields.List(
                            fields.String,
                            required=False,
                            description="Other diagram tools",
                        ),
                    },
                )
            ),
            "project_tracking": fields.String(
                required=False, description="Project tracking tool used by the project"
            ),
            "documentation": fields.Nested(
                ns.model(
                    "documentation",
                    {
                        "main": fields.List(
                            fields.String,
                            required=False,
                            description="Main documentation tool",
                        ),
                        "others": fields.List(
                            fields.String,
                            required=False,
                            description="Other documentation tools",
                        ),
                    },
                )
            ),
            "communication": fields.Nested(
                ns.model(
                    "communication",
                    {
                        "main": fields.List(
                            fields.String,
                            required=False,
                            description="Main communication tool",
                        ),
                        "others": fields.List(
                            fields.String,
                            required=False,
                            description="Other communication tools",
                        ),
                    },
                )
            ),
            "collaboration": fields.Nested(
                ns.model(
                    "collaboration",
                    {
                        "main": fields.List(
                            fields.String,
                            required=False,
                            description="Main collaboration tool",
                        ),
                        "others": fields.List(
                            fields.String,
                            required=False,
                            description="Other collaboration tools",
                        ),
                    },
                )
            ),
            "incident_management": fields.String(
                required=False, description="Incident management tool"
            ),
            "miscellaneous": fields.List(
                fields.Nested(
                    ns.model(
                        "MiscellaneousTool",
                        {
                            "name": fields.String(
                                required=True, description="Tool name"
                            ),
                            "description": fields.String(
                                required=True, description="Tool description"
                            ),
                        },
                    ),
                    required=False,
                    description="List of miscellaneous tools",
                )
            ),
        },
    )

    project_model = ns.model(
        "Project",
        {
            "user": fields.List(
                fields.Nested(user_model), required=True, description="List of users"
            ),
            "details": fields.List(
                fields.Nested(details_model),
                required=True,
                description="Details of project",
            ),
            "developed": fields.List(
                fields.String, required=False, description="Development details"
            ),
            "source_control": fields.List(
                fields.Nested(source_control_model),
                required=False,
                description="Source control platforms",
            ),
            "architecture": fields.Nested(
                architecture_model, required=False, description="Architecture details"
            ),
            "stage": fields.String(
                required=False, description="Stage status of the project"
            ),
            "supporting_tools": fields.Nested(
                supporting_tools_model,
                required=False,
                description="Supporting Tools Details",
            ),
        },
    )

    return project_model


def get_refresh_model():
    from .resources import ns

    refresh_model = ns.model(
        "Refresh",
        {"refresh_token": fields.String(required=True, description="Refresh token")},
    )
    return refresh_model
