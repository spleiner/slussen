# Contributing to SLussen

Thank you for your interest in contributing to SLussen! This document provides guidelines for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Submitting Changes](#submitting-changes)
- [Code Style](#code-style)
- [Testing](#testing)
- [Documentation](#documentation)

## Code of Conduct

This project adheres to a code of conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to [stefan@pleiner.se](mailto:stefan@pleiner.se).

### Our Standards

- Be respectful and inclusive
- Focus on constructive feedback
- Show empathy towards other community members
- Respect differing viewpoints and experiences

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- A GitHub account

### Development Setup

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/slussen.git
   cd slussen
   ```

3. **Add the upstream repository**:
   ```bash
   git remote add upstream https://github.com/spleiner/slussen.git
   ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install ruff  # For linting and formatting
   ```

5. **Test the setup**:
   ```bash
   streamlit run slussen.py
   ```

## Making Changes

### Branch Strategy

1. **Create a feature branch** from main:
   ```bash
   git checkout main
   git pull upstream main
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** in logical commits
3. **Keep your branch updated** with upstream main

### Types of Contributions

We welcome various types of contributions:

- **Bug fixes**: Fix issues or incorrect behavior
- **Feature enhancements**: Add new functionality
- **Documentation**: Improve or add documentation
- **Performance improvements**: Optimize code performance
- **UI/UX improvements**: Enhance user experience
- **Translation**: Add or improve Swedish/English translations

### Commit Guidelines

- Use clear, descriptive commit messages
- Start with a verb in present tense ("Add", "Fix", "Update")
- Keep the first line under 50 characters
- Reference issues when applicable

Example:
```
Add filtering by bus stop location

- Allows users to filter departures by specific stops
- Adds new checkbox controls to the sidebar
- Fixes issue #123
```

## Submitting Changes

### Pull Request Process

1. **Ensure your code passes all checks**:
   ```bash
   ruff check .
   ruff format --check .
   ```

2. **Run the application** to verify functionality:
   ```bash
   streamlit run slussen.py
   ```

3. **Push your branch** to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

4. **Create a Pull Request** on GitHub:
   - Use a descriptive title
   - Provide a detailed description of changes
   - Reference any related issues
   - Include screenshots if UI changes are involved

### Pull Request Template

When creating a PR, please include:

```markdown
## Description
Brief description of what this PR does.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Other (please describe)

## Testing
- [ ] I have tested these changes locally
- [ ] The application runs without errors
- [ ] All existing functionality still works

## Screenshots (if applicable)
Add screenshots for UI changes.

## Related Issues
Fixes #(issue number)
```

## Code Style

This project uses [Ruff](https://docs.astral.sh/ruff/) for linting and formatting.

### Key Guidelines

- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and reasonably sized
- Use type hints where appropriate

### Running Code Quality Checks

```bash
# Check for linting issues
ruff check .

# Format code
ruff format .

# Check if code is properly formatted
ruff format --check .
```

### Docstring Style

Use Google-style docstrings:

```python
def fetch_departure_data():
    """
    Fetch and parse departure information for all specified sites.
    
    Returns:
        list: A list of departure dictionaries sorted by expected time.
        
    Raises:
        Exception: If data cannot be fetched after multiple retries.
    """
```

## Testing

Currently, the project doesn't have formal unit tests, but manual testing is required:

### Manual Testing Checklist

- [ ] Application starts without errors
- [ ] Departure data loads correctly
- [ ] Bus line filtering works
- [ ] Traffic disruptions display when present
- [ ] Refresh functionality works
- [ ] UI is responsive on different screen sizes

### Adding Tests (Future)

If you're interested in adding automated tests:
- Use `pytest` for unit tests
- Test API integration with mock responses
- Test UI components where possible
- Ensure tests run in CI/CD pipeline

## Documentation

### Code Documentation

- Add docstrings to all new functions
- Update existing docstrings if behavior changes
- Use clear, concise language
- Include examples in docstrings where helpful

### User Documentation

- Update README.md for new features
- Add troubleshooting entries for common issues
- Include screenshots for UI changes
- Ensure both Swedish and English documentation is updated

### API Documentation

When working with external APIs:
- Document API endpoints used
- Note any rate limiting or usage restrictions
- Include example responses
- Document error handling

## Questions and Support

### Getting Help

- **Documentation**: Check the README.md first
- **Issues**: Search existing GitHub issues
- **Discussions**: Use GitHub Discussions for questions
- **Contact**: Reach out to [stefan@pleiner.se](mailto:stefan@pleiner.se)

### Reporting Bugs

When reporting bugs, please include:
- Clear description of the issue
- Steps to reproduce
- Expected vs actual behavior
- Browser and OS information
- Console errors (if any)
- Screenshots (if applicable)

### Suggesting Features

For feature requests:
- Check if a similar request already exists
- Clearly describe the feature and its benefits
- Consider the scope and complexity
- Be open to discussion and feedback

## Recognition

Contributors will be recognized in:
- GitHub contributors list
- Release notes (for significant contributions)
- README.md acknowledgments section (coming soon)

Thank you for contributing to SLussen! Your efforts help make public transport information more accessible to everyone.