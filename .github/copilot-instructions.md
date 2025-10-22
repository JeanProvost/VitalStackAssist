# GitHub Copilot Instructions for VitalStackAssist

## Project Overview
VitalStackAssist is a Python-based application that provides AI-powered assistance for healthcare vital signs monitoring and analysis.

## Code Style and Standards

### Python
- Follow PEP 8 style guidelines
- Use type hints for function parameters and return values
- Write docstrings for all public functions, classes, and modules (Google style)
- Keep functions focused and single-purpose
- Use meaningful variable and function names

### Project Structure
- `/src/ai/` - AI and machine learning components
- `/src/api/` - API endpoints and routing
- `/src/core/` - Core business logic
- `/src/models/` - Data models and schemas
- `/src/services/` - Service layer implementations

## Best Practices

### Error Handling
- Use specific exception types rather than generic Exception
- Always log errors with appropriate context
- Provide meaningful error messages for debugging

### Testing
- Write unit tests for new functionality
- Follow existing test patterns in the codebase
- Ensure tests are isolated and repeatable

### Documentation
- Comment complex algorithms or non-obvious code
- Keep comments concise and focused on "why" not "what"
- Update documentation when modifying functionality

### Dependencies
- Add new dependencies to requirements.txt
- Prefer well-maintained libraries with active communities
- Document any special installation requirements

## Security Considerations
- Never commit sensitive data or credentials
- Validate all user inputs
- Use environment variables for configuration
- Follow HIPAA compliance guidelines for healthcare data

## Docker
- Keep Dockerfile optimized for layer caching
- Use multi-stage builds when appropriate
- Document any Docker-specific configuration

## AI/ML Components
- Document model versions and training data requirements
- Include performance metrics and validation approaches
- Consider inference time and resource requirements

## API Development
- Follow RESTful conventions
- Version APIs appropriately
- Document endpoints with clear examples
- Include proper error responses

## When Suggesting Code
- Prioritize maintainability and readability
- Consider performance implications for healthcare data
- Ensure compatibility with existing codebase patterns
- Suggest improvements to code quality when appropriate
