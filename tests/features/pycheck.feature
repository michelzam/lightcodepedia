Feature: The course's files run as written — doctest and Dr. mypy in the page
  Michel, 2026-10-26, Python Module 09: "stick with my examples". The
  browser Python keeps no docstrings and has no doctest or mypy, so the
  runner reads them from the program's text: doctest.testmod() prints
  CPython's report, __doc__ and help() answer, mypy.api.run() and the
  🩺 button give mypy's verdict — and a pad's python fence wears it too.

  Background:
    Given I have a clean browser page

  Scenario: A failing example reports Expected and Got, as CPython does
    When I navigate to "/components/run"
    And I wait for the page to be interactive
    And I wait for the selector "#lc-pyrun-first_run .lc-pyrun-code"
    And I replace the "first_run" editor's program with:
      '''
      def jump(start: int, leap: int) -> int:
          """
          Makes an absolute jump from start.

          >>> jump(2, 3)
          5
          >>> jump(1, -1)
          2
          """
          return start + leap


      if __name__ == "__main__":
          import doctest
          doctest.testmod()
          print("done")
      '''
    And I click Run in the "first_run" editor
    Then the "first_run" editor's output shows:
      '''
      File "first_run.py", line 7, in __main__.jump
      Failed example:
          jump(1, -1)
      Expected:
          2
      Got:
          0
      '''
    And the "first_run" editor's output shows "***Test Failed*** 1 failure."

  Scenario: Classes and methods are doctested verbosely, objects built first
    When I navigate to "/components/run"
    And I wait for the page to be interactive
    And I wait for the selector "#lc-pyrun-first_run .lc-pyrun-code"
    And I replace the "first_run" editor's program with:
      '''
      class Pet:
          """A simple pet class.
          >>> p = Pet("Luna")
          >>> isinstance(p, Pet)
          True
          """

          def __init__(self, name: str):
              self.name = name

          def greet(self) -> str:
              """
              >>> p = Pet("Luna")
              >>> p.greet()
              'Hello, I am Luna!'
              """
              return f"Hello, I am {self.name}!"


      if __name__ == "__main__":
          import doctest
          doctest.testmod(verbose=True)
          print(Pet.__doc__.split(".")[0])
          help(Pet.greet)
      '''
    And I click Run in the "first_run" editor
    Then the "first_run" editor's output shows:
      '''
      Trying:
          p = Pet("Luna")
      Expecting nothing
      ok
      '''
    And the "first_run" editor's output shows "2 tests in __main__.Pet.greet"
    And the "first_run" editor's output shows "Test passed."
    And the "first_run" editor's output shows "A simple pet class"
    And the "first_run" editor's output shows "greet(self) -> str"
    When I click Test in the "first_run" editor
    Then the "first_run" editor's tests read "4 passed, 0 failed"

  Scenario: The PythonAnywhere mypy recipe runs, and its verdict follows the hint
    When I navigate to "/components/run"
    And I wait for the page to be interactive
    And I wait for the selector "#lc-pyrun-mypy_demo .lc-pyrun-code"
    And I click Run in the "mypy_demo" editor
    Then the "mypy_demo" editor's output shows "mypy_demo.py:1: error: Function is missing a return type annotation  [no-untyped-def]"
    And the "mypy_demo" editor's output shows "❌ Dr. mypy:"
    When I press Dr. mypy in the "mypy_demo" editor
    Then the "mypy_demo" editor's output shows "Found 1 error in 1 file (checked 1 source file)"
    When I replace "cut: float):" with "cut: float) -> float:" in the "mypy_demo" editor
    And I click Run in the "mypy_demo" editor
    Then the "mypy_demo" editor's output shows "✅ Dr. mypy: no type errors"
    When I press Dr. mypy in the "mypy_demo" editor
    Then the "mypy_demo" editor's output shows "✅ Dr. mypy (lite): no type errors"

  Scenario: Dr. mypy speaks mypy's words, and judges only what is written
    When I navigate to "/components/run"
    And I wait for the page to be interactive
    And I wait for the selector "#lc-pyrun-mypy_demo .lc-pyrun-code"
    And I replace the "mypy_demo" editor's program with:
      '''
      def jump(start: int, leap: int) -> int:
          return 'far'


      def say() -> None:
          return 3


      class Pet:
          def __init__(self, name: str) -> None:
              self.name = name


      print(jump('2', 3), jump(2, leap=1.5))  # jump('x', 1) in a comment
      lucky = Pet(3)
      ok = Pet(input("name? "))
      s = "jump('x', 1)"
      '''
    And I press Dr. mypy in the "mypy_demo" editor
    Then the "mypy_demo" editor's output shows:
      '''
      mypy_demo.py:2: error: Incompatible return value type (got "str", expected "int")  [return-value]
      '''
    And the "mypy_demo" editor's output shows "mypy_demo.py:6: error: No return value expected  [return-value]"
    And the "mypy_demo" editor's output shows "mypy_demo.py:14: error: Argument 1 to \"jump\" has incompatible type \"str\"; expected \"int\"  [arg-type]"
    And the "mypy_demo" editor's output shows "mypy_demo.py:14: error: Argument \"leap\" to \"jump\" has incompatible type \"float\"; expected \"int\"  [arg-type]"
    And the "mypy_demo" editor's output shows "mypy_demo.py:15: error: Argument 1 to \"Pet\" has incompatible type \"int\"; expected \"str\"  [arg-type]"
    And the "mypy_demo" editor's output shows "Found 5 errors in 1 file (checked 1 source file)"

  Scenario: A pad's python fence wears Dr. mypy's verdict in its gutter
    When I navigate to "/components/mdpad"
    And I wait for the page to be interactive
    Then the "typed_pad" pad marks lines "8" as errors
    And under the "typed_pad" pad it says "line 8" and "Function is missing a return type annotation"

  Scenario: The stand-in loads in every browser the class uses
    Michel, 2026-10-26, from his runner: "ImportError: no module named
    'doctest'" — the page ran without the stand-in. One regex lookbehind
    is enough for a Safari before 16.4 to refuse the whole engine piece.
    When I navigate to "/components/run"
    And I wait for the page to be interactive
    Then the page carries the doctest stand-in
    And the engine file "docs/_includes/pycheck.md" uses no regex lookbehind

  Scenario: A pad doctests its python fences as you write — no main block, no testmod
    Michel, 2026-10-26: "doctest in the gutter … in the mdpad, I prefer not
    to add a if __main__ … and not to call explicitly doctest".
    When I navigate to "/components/mdpad"
    And I wait for the page to be interactive
    Then the "doctest_pad" pad marks lines "10" as errors
    And under the "doctest_pad" pad it says "line 10" and "doctest: jump(1, -1) → got 0, expected 2"
    And the "doctest_pad" pad counts "1/2" examples passing
    When I replace "    >>> jump(1, -1)\n    2" with "    >>> jump(1, -1)\n    0" in the "doctest_pad" pad
    Then the "doctest_pad" pad counts "2/2" examples passing
    And the "doctest_pad" pad marks no line as an error
