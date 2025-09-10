# Contributing to Django Bookstore

Thank you for your interest in contributing to Django Bookstore! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### Reporting Issues
- Use the GitHub issue tracker
- Provide detailed information about the bug or feature request
- Include steps to reproduce for bugs
- Use appropriate labels

### Suggesting Features
- Open an issue with the "enhancement" label
- Describe the feature and its benefits
- Consider implementation complexity
- Discuss with maintainers before major changes

### Code Contributions
- Fork the repository
- Create a feature branch
- Make your changes
- Add tests if applicable
- Submit a pull request

## 🛠️ Development Setup

### Prerequisites
- Python 3.11+
- PostgreSQL 13+
- Git
- Docker (optional)

### Setup Steps
1. Fork and clone the repository
2. Create a virtual environment
3. Install dependencies: `pip install -r requirements.txt`
4. Set up environment variables (copy `env.example` to `.env`)
5. Run migrations: `python manage.py migrate`
6. Create a superuser: `python manage.py createsuperuser`
7. Start the development server: `python manage.py runserver`

### Docker Setup
```bash
docker compose up -d --build
```

## 📝 Code Style

### Python Code
- Follow PEP 8 style guidelines
- Use Black for code formatting
- Use isort for import sorting
- Maximum line length: 88 characters

### JavaScript Code
- Use consistent indentation (2 spaces)
- Use meaningful variable names
- Add comments for complex logic
- Follow modern ES6+ practices

### HTML/CSS
- Use semantic HTML
- Follow Tailwind CSS conventions
- Ensure accessibility compliance
- Use consistent class naming

## 🧪 Testing

### Running Tests
```bash
# Run all tests
python manage.py test

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

### Writing Tests
- Write tests for new features
- Test both success and error cases
- Use descriptive test names
- Mock external dependencies

### Test Structure
```
tests/
├── test_models.py
├── test_views.py
├── test_serializers.py
└── test_management.py
```

## 📋 Pull Request Process

### Before Submitting
- [ ] Code follows style guidelines
- [ ] Tests pass locally
- [ ] Documentation updated if needed
- [ ] No merge conflicts
- [ ] Commit messages are clear

### Pull Request Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests added/updated
- [ ] All tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
```

### Review Process
- Maintainers will review all pull requests
- Address feedback promptly
- Keep pull requests focused and small
- Respond to review comments

## 🏗️ Architecture Guidelines

### Django Best Practices
- Use Django's built-in features
- Follow Django's security guidelines
- Use proper model relationships
- Implement proper error handling

### API Design
- Follow RESTful principles
- Use appropriate HTTP status codes
- Implement proper pagination
- Add comprehensive error handling

### Frontend Guidelines
- Use progressive enhancement
- Ensure mobile responsiveness
- Implement proper loading states
- Handle errors gracefully

## 🐛 Bug Reports

### Bug Report Template
```markdown
**Describe the bug**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected behavior**
What you expected to happen.

**Screenshots**
If applicable, add screenshots.

**Environment:**
- OS: [e.g. Ubuntu 20.04]
- Python version: [e.g. 3.11]
- Django version: [e.g. 5.2.5]
- Browser: [e.g. Chrome 91]

**Additional context**
Any other context about the problem.
```

## ✨ Feature Requests

### Feature Request Template
```markdown
**Is your feature request related to a problem?**
A clear description of what the problem is.

**Describe the solution you'd like**
A clear description of what you want to happen.

**Describe alternatives you've considered**
Alternative solutions or features you've considered.

**Additional context**
Any other context or screenshots about the feature request.
```

## 📚 Documentation

### Documentation Guidelines
- Keep documentation up to date
- Use clear, concise language
- Include code examples
- Update README files as needed

### Documentation Types
- API documentation
- Setup guides
- Feature documentation
- Troubleshooting guides

## 🔒 Security

### Security Guidelines
- Never commit secrets or credentials
- Use environment variables for configuration
- Follow Django security best practices
- Report security issues privately

### Security Issues
For security-related issues, please email security@example.com instead of creating a public issue.

## 🏷️ Release Process

### Version Numbering
We use semantic versioning (MAJOR.MINOR.PATCH):
- MAJOR: Breaking changes
- MINOR: New features (backward compatible)
- PATCH: Bug fixes (backward compatible)

### Release Checklist
- [ ] All tests pass
- [ ] Documentation updated
- [ ] Version numbers updated
- [ ] Changelog updated
- [ ] Release notes prepared

## 🤔 Questions?

### Getting Help
- Check existing issues and discussions
- Join our community chat (if available)
- Contact maintainers directly
- Read the documentation

### Community Guidelines
- Be respectful and inclusive
- Help others when possible
- Follow the code of conduct
- Provide constructive feedback

## 📄 License

By contributing to Django Bookstore, you agree that your contributions will be licensed under the MIT License.

## 🙏 Recognition

Contributors will be recognized in:
- CONTRIBUTORS.md file
- Release notes
- Project documentation

Thank you for contributing to Django Bookstore! 🎉
