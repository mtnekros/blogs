// Dart Cheat Sheet

// Hello World
void main() {
  print("Hello, World!");
}

// Variables
var name = "John";
int age = 30;
double height = 5.11;
bool isStudent = true;
final piValue = 3.14159265359;
const apiKey = "your_api_key";

// Data Types
// - Numbers: int, double
// - Strings: String
// - Booleans: bool
// - Lists: List
// - Maps: Map

// String Operations
String greeting = "Hello";
String name = "Alice";
String message = greeting + " " + name; // Concatenation
String interpolated = "$greeting $name"; // String interpolation

// Lists
List<String> colors = ["Red", "Green", "Blue"];
colors.add("Yellow");
colors.remove("Green");
colors[0] = "Purple";

// Maps
Map<String, int> scores = {
  "Math": 90,
  "Science": 85,
};
scores["English"] = 88;
scores.remove("Science");

// Control Structures
if (condition) {
  // code to execute if the condition is true
} else {
  // code to execute if the condition is false
}

for (int i = 0; i < 5; i++) {
  // loop code
}

while (condition) {
  // loop code
}

switch (value) {
  case 'A':
    // code for A
    break;
  case 'B':
    // code for B
    break;
  default:
    // code for other cases
}

// Functions
int add(int a, int b) {
  return a + b;
}

// Optional Parameters
void printMessage(String message, [String? name]) {
  if (name != null) {
    print("$message, $name");
  } else {
    print(message);
  }
}

// Named Parameters
void printDetails({String? name, int? age}) {
  print("Name: $name, Age: $age");
}

// Classes and Objects
class Person {
  String name = "";
  int age = 0;

  Person(this.name, this.age);

  void introduceYourself() {
    print("Hello, my name is $name, and I am $age years old.");
  }
}

void main() {
  Person person = Person("Alice", 25);
  person.introduceYourself();
}

// Inheritance
class Student extends Person {
  String major = "";

  Student(String name, int age, this.major) : super(name, age);

  @override
  void introduceYourself() {
    print("I'm a student. My name is $name, and I'm majoring in $major.");
  }
}

void main() {
  Student student = Student("Bob", 20, "Computer Science");
  student.introduceYourself();
}

// Libraries
import 'dart:math'; // Import the math library

void main() {
  print(sqrt(25)); // Using a function from the math library
}
