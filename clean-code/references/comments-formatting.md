# Comments and Formatting

Comprehensive guide to comment discipline and code formatting. Based on Robert C. Martin's *Clean Code*, Chapters 4 and 5.


## Table of Contents
1. [The Truth About Comments](#the-truth-about-comments)
2. [Good Comments](#good-comments)
3. [Bad Comments](#bad-comments)
4. [Formatting](#formatting)
5. [When Comments Are Truly Necessary](#when-comments-are-truly-necessary)

---

## The Truth About Comments

**Don't comment bad code -- rewrite it.** Comments are, at best, a necessary evil. The proper use of comments is to compensate for our failure to express ourselves in code. Every time you write a comment, you should grimace and feel the failure of your ability of expression.

Comments lie. Not always, and not intentionally, but too often. Code changes and evolves; comments don't always follow. The older a comment is and the farther it is from the code it describes, the more likely it is to be wrong.

---

## Good Comments

Not all comments are bad. Some are necessary and valuable. Here are the types worth writing:

### Legal Comments

Copyright and license headers mandated by corporate or legal standards.

```java
// Copyright (c) 2024 Acme Corp. All rights reserved.
// Licensed under the Apache License, Version 2.0
```

Keep them short. Reference a standard license file rather than embedding the full text.

### Informative Comments

Provide information that cannot be expressed in the code itself.

```java
// Format: kk:mm:ss EEE, MMM dd, yyyy
Pattern timeMatcher = Pattern.compile("\\d*:\\d*:\\d* \\w*, \\w* \\d*, \\d*");
```

Even here, a named constant or custom type could eliminate the need: `TIMESTAMP_PATTERN`.

### Explanation of Intent

Explain *why* a decision was made, not *what* the code does.

```python
# We sort by creation date descending because the business requirement
# specifies that the most recently created items appear first in the
# dashboard, even though alphabetical would be more intuitive.
items.sort(key=lambda x: x.created_at, reverse=True)
```

This is valuable because the *what* is visible in the code, but the *why* would otherwise be lost.

### Warning of Consequences

Alert other developers about consequences that are not obvious.

```java
// Don't run this test in CI -- it takes 45 minutes and requires
// a live connection to the production payment gateway
@Ignore("Long-running integration test requiring production access")
public void testLivePaymentGateway() { ... }
```

### TODO Comments

Mark work that needs to be done but cannot be done right now.

```python
# TODO(#1234): Replace with proper caching once Redis is provisioned
def get_user_preferences(user_id):
    return db.query(f"SELECT * FROM preferences WHERE user_id = {user_id}")
```

**Rules for TODOs:**
- Include a ticket number or issue reference
- Scan and resolve them regularly (they are not permanent)
- Never use TODO as an excuse to leave broken code
- IDE/linter plugins can track and report outstanding TODOs

### Amplification

Emphasize the importance of something that might otherwise seem inconsequential.

```java
String listItemContent = match.group(3).trim();
// The trim is critically important. It removes trailing whitespace
// that would cause the item to be recognized as another list.
new ListItemWidget(this, listItemContent, this.level + 1);
```

---

## Bad Comments

Most comments fall into these categories and should be eliminated:

### Mumbling

Comments written because "you should comment" rather than because they add value.

```java
// The processor
private Processor processor;

// Default constructor
public MyClass() { }
```

These say nothing. Delete them.

### Redundant Comments

Comments that take longer to read than the code they describe.

```java
// Returns the day of the month
public int getDayOfMonth() {
    return dayOfMonth;
}

// Check if the employee is eligible for benefits
if (employee.isEligibleForBenefits()) { ... }
```

The code already says exactly this. The comment is noise.

### Misleading Comments

Comments that are subtly incorrect -- the most dangerous kind.

```java
// Returns true if the user is active
public boolean isActive() {
    return lastLoginDate != null && !isDeleted && subscriptionEndDate.isAfter(now());
}
```

The comment says "active" means logged in before. The code checks three conditions. When the code changes and the comment doesn't, a future developer will be misled.

### Mandated Comments

Rules that require every function or variable to have a comment produce noise.

```java
/**
 * The name.
 * @param name The name.
 */
public void setName(String name) {
    this.name = name;
}
```

This adds no information. It's clutter that developers learn to ignore, which means they'll also ignore the few comments that actually matter.

### Journal Comments

Changelog entries at the top of files.

```java
// 2024-01-15 - Added validation for email format
// 2024-01-20 - Fixed bug in email regex
// 2024-02-01 - Added support for international emails
```

This is what version control is for. `git log` and `git blame` provide this information with more accuracy and context.

### Commented-Out Code

```python
# user_cache = {}
# def get_cached_user(user_id):
#     if user_id not in user_cache:
#         user_cache[user_id] = db.get_user(user_id)
#     return user_cache[user_id]

def get_user(user_id):
    return db.get_user(user_id)
```

Other developers are afraid to delete commented-out code because they think it must be there for a reason. It accumulates like barnacles. **Delete it.** Version control has perfect memory.

### Noise Comments

Comments that restate the obvious in a different form.

```java
/** Default constructor */
protected AnnualDateRule() { }

/** The day of the month */
private int dayOfMonth;

/** Returns the day of the month
 * @return the day of the month */
public int getDayOfMonth() { return dayOfMonth; }
```

Every one of these is noise. They provide no information, train developers to ignore comments, and create a false sense of documentation thoroughness.

### Position Markers and Banners

```java
// ========== PRIVATE METHODS ==========
// --- Validation ---
// /////// Constructor ///////
```

If your file is so large that you need position markers, the file is too large. Extract classes instead of adding banners.

### Closing Brace Comments

```java
if (condition) {
    while (running) {
        for (item : items) {
            // ... lots of code ...
        } // for
    } // while
} // if
```

If you need comments to track closing braces, your function is too long. Extract methods until the structure is obvious.

### Attribution Comments

```java
// Added by: john.smith@company.com
```

Version control tracks authorship more reliably. Use `git blame`.

---

## Formatting

### Why Formatting Matters

Code formatting is about communication, and communication is the professional developer's first order of business. The formatting of your code communicates important information long after the original developer has moved on.

### Vertical Formatting

#### The Newspaper Metaphor

Source files should be organized like a newspaper article:
- **Name** should be simple but explanatory (the headline)
- **Top** should provide high-level concepts and algorithms (the synopsis)
- **Bottom** should contain the lowest-level functions and details (the body)

#### Vertical Openness Between Concepts

Each group of related lines represents a complete thought. Separate thoughts with blank lines.

```python
# GOOD: Blank lines separate concepts
import os
import sys

from myapp.models import User
from myapp.services import EmailService


class UserRegistration:

    def __init__(self, email_service):
        self.email_service = email_service

    def register(self, name, email):
        user = User.create(name=name, email=email)
        self.email_service.send_welcome(user)
        return user
```

```python
# BAD: Everything runs together
import os
import sys
from myapp.models import User
from myapp.services import EmailService
class UserRegistration:
    def __init__(self, email_service):
        self.email_service = email_service
    def register(self, name, email):
        user = User.create(name=name, email=email)
        self.email_service.send_welcome(user)
        return user
```

#### Vertical Density

Lines that are tightly related should appear close together vertically. Don't insert blank lines between closely related lines.

```java
// BAD: Useless comments break vertical density
public class ReporterConfig {

    /**
     * The class name of the reporter listener
     */
    private String className;

    /**
     * The properties of the reporter listener
     */
    private List<Property> properties = new ArrayList<>();
}

// GOOD: Dense, related declarations together
public class ReporterConfig {
    private String className;
    private List<Property> properties = new ArrayList<>();
}
```

#### Vertical Distance

Closely related concepts should be kept vertically close to each other. Don't force the reader to hop around the file.

**Rules:**
- **Local variables:** Declare at the top of the function or as close to first usage as practical
- **Instance variables:** Declare at the top of the class (everyone needs to know about them)
- **Dependent functions:** The caller should be above the callee, and they should be close
- **Conceptual affinity:** Functions that do similar things or operate on the same data should be near each other

#### Vertical Ordering

Function call dependencies should point downward: a function that is called should be below the function that calls it. This creates a nice flow from high-level to low-level, like reading a newspaper.

### Horizontal Formatting

#### Line Length

**Keep lines short.** The old 80-character limit is a reasonable guideline. Modern screens can show more, but readability drops beyond 100-120 characters. Scrolling horizontally breaks the reader's flow.

#### Horizontal Openness and Density

Use whitespace to associate strongly related things and disassociate weakly related things.

```java
// Spaces around assignment (weak association between sides)
int lineCount = countLines();

// No space between function name and parenthesis (strong association)
lineCount = countLines();

// Spaces around binary operators by precedence
return b*b - 4*a*c;  // Multiplication is higher precedence, tighter
return (-b + determinant) / (2*a);
```

#### Indentation

Indentation makes the scope hierarchy visible. Each level of nesting gets one indentation level. **Never break this rule, even for short `if` statements or tiny loops.**

```java
// BAD: Collapsed scopes hide structure
if (condition) return true;

// GOOD: Indentation preserved
if (condition) {
    return true;
}
```

### Team Rules

**A team should agree on a single formatting style and everyone should use it.** Individual style preferences must yield to the team standard.

The best way to enforce team rules:

| Approach | Tool examples | Benefit |
|----------|---------------|---------|
| **Automated formatter** | Prettier, Black, gofmt, rustfmt | Eliminates all style debates |
| **Linter with auto-fix** | ESLint, Pylint, RuboCop | Catches style and quality issues |
| **Pre-commit hooks** | Husky, pre-commit, lefthook | Prevents style violations from entering repo |
| **CI enforcement** | Format check in pipeline | Catches anything hooks miss |
| **EditorConfig** | `.editorconfig` file | Consistent settings across editors |

**The best formatting rule:** Use an automated formatter and never think about formatting again. Time spent debating tabs versus spaces is time not spent writing clean code.

---

## When Comments Are Truly Necessary

Despite the general advice to minimize comments, certain situations genuinely require them:

| Situation | Why code alone isn't enough | Example |
|-----------|---------------------------|---------|
| **Regulatory requirement** | Law/compliance requires documentation | HIPAA, SOX, GDPR compliance notes |
| **Non-obvious performance choice** | Algorithm choice isn't self-evident | "Using radix sort here because n > 10M and keys are bounded" |
| **External system quirk** | Workaround for third-party bug | "API returns 200 for errors; we check response body instead" |
| **Concurrency rationale** | Threading decisions need explanation | "Double-checked locking required here because..." |
| **Domain formula** | Mathematical formula from spec | "Amortization formula from IRS Publication 936" |
| **Public API contract** | Users cannot read implementation | Javadoc for library interfaces |

The key: comments should explain *why*, never *what*. If you find yourself explaining *what* the code does, the code needs to be clearer, not the comment.
