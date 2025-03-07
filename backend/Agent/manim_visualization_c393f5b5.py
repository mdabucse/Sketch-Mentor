from manim import *

class ReliableQuadraticFormula(Scene):
    def construct(self):
        try:
            # --- Configuration ---
            a_val = 1
            b_val = -3
            c_val = 2

            # --- Error Handling (Basic) ---
            if a_val == 0:
                raise ValueError("Coefficient 'a' cannot be zero for a quadratic equation.")

            # --- Title ---
            title = Tex("Visualizing the Quadratic Formula").to_edge(UP)
            self.play(Write(title))
            self.wait(1)

            # --- Quadratic Equation ---
            quadratic_eq_tex = MathTex("a", "x^2", "+", "b", "x", "+", "c", "=", "0")
            quadratic_eq_tex.set_color_by_tex("a", YELLOW)
            quadratic_eq_tex.set_color_by_tex("b", GREEN)
            quadratic_eq_tex.set_color_by_tex("c", BLUE)
            self.play(Write(quadratic_eq_tex))
            self.wait(2)

            # --- Introduce a, b, c values ---
            abc_values_text = VGroup(
                MathTex("a = ", str(a_val)).set_color_by_tex("a", YELLOW),
                MathTex("b = ", str(b_val)).set_color_by_tex("b", GREEN),
                MathTex("c = ", str(c_val)).set_color_by_tex("c", BLUE)
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(quadratic_eq_tex, DOWN, buff=0.5, aligned_edge=LEFT)

            self.play(FadeIn(abc_values_text))
            self.wait(2)

            # --- Quadratic Formula ---
            quadratic_formula_tex = MathTex(
                "x", "=",
                "\\frac{", "-b", " \\pm ", "\\sqrt{", "b^2", "-", "4ac", "} ", "}{", "2a", "}"
            )
            quadratic_formula_tex.set_color_by_tex("-b", GREEN)
            quadratic_formula_tex.set_color_by_tex("b^2", GREEN)
            quadratic_formula_tex.set_color_by_tex("4ac", VIOLET) # Combined for simplicity
            quadratic_formula_tex.set_color_by_tex("2a", YELLOW)

            quadratic_formula_tex.next_to(abc_values_text, DOWN, buff=0.7, aligned_edge=LEFT)
            self.play(Write(quadratic_formula_tex))
            self.wait(2)

            # --- Discriminant Calculation ---
            discriminant_formula_tex = MathTex("\\Delta = b^2 - 4ac")
            discriminant_formula_tex.set_color_by_tex("b^2", GREEN)
            discriminant_formula_tex.set_color_by_tex("4ac", VIOLET)
            discriminant_formula_tex.next_to(quadratic_formula_tex, DOWN, buff=0.7, aligned_edge=LEFT)
            self.play(Write(discriminant_formula_tex))
            self.wait(1.5)

            b_squared = b_val**2
            four_ac = 4 * a_val * c_val
            discriminant_value = b_squared - four_ac

            discriminant_value_tex = MathTex(
                "\\Delta = ", str(b_squared), "-", str(four_ac), "=", str(discriminant_value)
            )
            discriminant_value_tex.next_to(discriminant_formula_tex, DOWN, buff=0.3, aligned_edge=LEFT)
            self.play(Write(discriminant_value_tex))
            self.wait(2)

            # --- Square Root of Discriminant ---
            sqrt_discriminant_tex = MathTex("\\sqrt{\\Delta} = \\sqrt{", str(discriminant_value), "}")
            sqrt_discriminant_tex.next_to(discriminant_value_tex, DOWN, buff=0.7, aligned_edge=LEFT)
            self.play(Write(sqrt_discriminant_tex))
            self.wait(1.5)

            sqrt_discriminant_value = np.sqrt(discriminant_value) # Explicit numpy sqrt for reliability

            sqrt_discriminant_result_tex = MathTex(
                "\\sqrt{\\Delta} = ", str(sqrt_discriminant_value)
            )
            sqrt_discriminant_result_tex.next_to(sqrt_discriminant_tex, DOWN, buff=0.3, aligned_edge=LEFT)
            self.play(Write(sqrt_discriminant_result_tex))
            self.wait(2)

            # --- Solutions x1 and x2 ---
            x1_formula_tex = MathTex("x_1 = \\frac{-b + \\sqrt{\\Delta}}{2a}")
            x1_formula_tex.next_to(sqrt_discriminant_result_tex, DOWN, buff=0.7, aligned_edge=LEFT)
            self.play(Write(x1_formula_tex))
            self.wait(1.5)

            x2_formula_tex = MathTex("x_2 = \\frac{-b - \\sqrt{\\Delta}}{2a}")
            x2_formula_tex.next_to(x1_formula_tex, DOWN, buff=0.5, aligned_edge=LEFT)
            self.play(Write(x2_formula_tex))
            self.wait(1.5)

            # Calculate and display x1
            x1_numerator = -b_val + sqrt_discriminant_value
            x1_denominator = 2 * a_val
            x1_value = x1_numerator / x1_denominator # Explicit calculation

            x1_value_tex = MathTex(
                "x_1 = \\frac{", str(x1_numerator), "}{", str(x1_denominator), "} = ", str(x1_value)
            )
            x1_value_tex.next_to(x1_formula_tex, DOWN, buff=0.3, aligned_edge=LEFT)
            self.play(Write(x1_value_tex))
            self.wait(2)

            # Calculate and display x2
            x2_numerator = -b_val - sqrt_discriminant_value
            x2_denominator = 2 * a_val
            x2_value = x2_numerator / x2_denominator # Explicit calculation

            x2_value_tex = MathTex(
                "x_2 = \\frac{", str(x2_numerator), "}{", str(x2_denominator), "} = ", str(x2_value)
            )
            x2_value_tex.next_to(x2_value_tex.align_to(x1_value_tex, LEFT), DOWN, buff=0.3, aligned_edge=LEFT) # Align with x1 for visual clarity.
            self.play(Write(x2_value_tex))
            self.wait(3)

            # --- End Scene ---
            self.play(FadeOut(VGroup(*self.mobjects))) # Fade out all objects
            self.wait(1)


        except ValueError as e:
            error_text = Tex(f"Error: {e}").set_color(RED).to_screen_center()
            self.add(error_text) # Directly add to scene in case of error during animation setup.
            self.wait(5)
        except Exception as e:
            import traceback
            error_trace = traceback.format_exc()
            error_message = Tex(f"An unexpected error occurred:\n{str(e)}\n\nTraceback:\n{error_trace}").set_color(RED).scale(0.5).to_screen_center()
            self.add(error_message)
            self.wait(10)