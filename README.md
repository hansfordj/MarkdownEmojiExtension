# JSimpleValidation #

[MIT License]: https://opensource.org/licenses/MIT
[FluentValidation]: https://github.com/JeremySkinner/FluentValidation

JSimpleValidation is a small validation library for Java 1.8, that uses a fluent interface and lambda expressions for building validation rules. The project took a 
lot of inspiration from the great [FluentValidation], which is a great open source library for .NET.

## Why? ##

Validation of input data is one of the most important tasks in any sufficiently complex business application. You often need to validate user input against 
a given format, you have to check if imported data is valid or if incoming requests match certain rules.

And it doesn't end with the simple data validation. Often enough you want to generate custom error messages for validation errors. Or you want to assign a certain 
error enum (or state) to a given validation error. Or a property of an object is optional, and should only be validated when it exists. And so on, and so on...

If you are not having a consistent approach to the problem, your validation code turns into a nested-if massacre.

## Documentation ##

The JSimpleValidation User Guide is available at:

* [http://bytefish.github.io/JSimpleValidation/](http://bytefish.github.io/JSimpleValidation/) 

## Getting Started ##

Imagine a list of Persons should be stored in a database. The input data possibly contains invalid entities, 
that should not be persisted to the database, so they should be validated with `JSimpleValidation`_ first.

The Validation Rules are:

* Every Person should have a First Name, Last Name and a Birth Date.
* The length of the names shouldn't exceed 10 characters (which is an abritarily set limitation for the example).
* The birth date should be after the year ``1900`` (which is an abritarily set limitation for the example).

### Domain Model ###

The domain model in the Java application might look like this.

```java
public class Person {

    private String firstName;
    private String lastName;
    private LocalDate birthDate;

    public Person(String firstName, String lastName, LocalDate birthDate) {
        this.firstName = firstName;
        this.lastName = lastName;
        this.birthDate = birthDate;
    }

    public String getFirstName() {
        return firstName;
    }

    public String getLastName() {
        return lastName;
    }

    public LocalDate getBirthDate() {
        return birthDate;
    }

}
```

### Validator ###

The basic idea of JSimpleValidation is to define rules on each property of your domain model. You can chain multiple rules by 
using its Fluent interface, which makes it easy to build and understand the validation rules.

Every Validator in JSimpleValidation is an ``AbstractValidator<TEntity>``. The ``AbstractValidator`` base class has a 
method ``ruleFor``, which takes a lambda expression (the property of your entity) and exposes a Fluent interface for adding 
validation rules.

```java
public class PersonValidator extends AbstractValidator<Person> {

    public PersonValidator() {
        super();

        ruleFor(Person::getFirstName)
                .add(new NotNullOrWhitespacePredicate())
                .add(new StringLengthPredicate(0, 10));

        ruleFor(Person::getLastName)
                .add(new NotNullOrWhitespacePredicate())
                .add(new StringLengthPredicate(0, 10));

        ruleFor(Person::getBirthDate)
                .add(new NotNullPredicate())
                .add(new DateAfterPredicate(LocalDate.of(1900, 1, 1)));
    }

}
```

You can see, that a Rule consists of chaining multiple predicates by using the ``add`` method on it. A Predicate in mathematics is basically a statement, 
that may be true or false depending on its input. The Predicates in JSimpleValidation are in the Namespace ``de.bytefish.jsimplevalidation.predicates``
namespace.

In the example we are applying a ``NotNullOrWhitespacePredicate`` and a ``StringLengthPredicate`` on the first and last name. The ``NotNullOrWhitespacePredicate``
validates, that a property is not null or consists of whitespaces only. The ``StringLengthPredicate`` makes sure, that a string length is in the given range. The birth date is 
validated with ``NotNullPredicate``, which checks if the given property is not null and a ``DateAfterPredicate`` predicate, which checks if the given date is after 
a specified date.

### Validating Entities ###

What's left is to validate an entity against the specified rules. This is simply done by instantiating a ``PersonValidator`` and use the ``validate`` method on it.

The result of checking a valid entity is an empty list of Validation errors. The sample entity has valid values for the first name, last name and birth date:

```java
@Test
public void TestValidator_WithoutError() {
    // Instantiate the Validator:
    PersonValidator personValidator = new PersonValidator();
    // Create a valid person:
    Person p0 = new Person("Philipp", "Wagner", LocalDate.of(1986, 5, 12));
    // Validate the etity, which returns a list of validation errors:
    List<ValidationError> validationErrors = personValidator.validate(p0);
    // Assert, that the Validator returns no errors:
    Assert.assertEquals(0, validationErrors.size());
}
```
    
Next an invalid entity can be checked. The sample entity misses the first name (empty string), the last name is too long and the birthdate is before ``1900``. This will 
lead to 3 validation errors.

```java
@Test
public void TestValidator_Errors() {
    // Instantiate the Validator:
    PersonValidator personValidator = new PersonValidator();
    // Create a valid person:
    Person p0 = new Person("", "Wagner-Meier-Heinrich", LocalDate.of(1812, 1, 12));
    // Validate the etity, which returns a list of validation errors:
    List<ValidationError> validationErrors = personValidator.validate(p0);
    // Assert, that the Validator returns no errors:
    Assert.assertEquals(3, validationErrors.size());
}
```