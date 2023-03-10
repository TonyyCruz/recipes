from unittest.mock import patch

from django.urls import resolve, reverse

from recipes import views

from .test_testcase_with_recipe import TestCaseWithRecipe


class RecipesListViews(TestCaseWithRecipe):
    def test_recipe_list_uses_correct_view(self):
        view = resolve(reverse("recipes:list"))
        self.assertIs(views.recipe_list, view.func)

    def test_recipe_list_template_shows_no_recipes_found_if_no_recipes(self):
        response = self.client.get(reverse("recipes:list"))
        self.assertIn(
            "<h1>There are no recipes yet</h1>",
            response.content.decode("utf-8")
        )

    def test_recipe_list_loads_recipe(self):
        self.make_recipe()
        response = self.client.get(reverse("recipes:list"))
        content = response.content.decode("utf-8")
        response_context_recipes = response.context['recipes']

        self.assertIn("My test title", content)
        self.assertIn("10 minutos", content)
        self.assertIn("3 porcoes", content)
        self.assertEqual(len(response_context_recipes), 1)

    def test_recipe_list_no_published_recipes_not_appear(self):
        self.make_recipe(is_published=False)
        response = self.client.get(reverse("recipes:list"))
        content = response.content.decode("utf-8")

        self.assertIn("There are no recipes yet", content)

    def test_recipe_list_have_a_correct_pagination_range(self):
        """slow"""
        self.make_multiples_recipes(18)
        with patch("recipes.views.ITEMS_PER_PAGE", new=3):
            response = self.client.get(reverse("recipes:list") + "?page=1")
            response_2 = self.client.get(reverse("recipes:list") + "?page=3")
            response_3 = self.client.get(reverse("recipes:list") + "?page=4")

            context = response.context["pagination_range"]
            context_2 = response_2.context["pagination_range"]
            context_3 = response_3.context["pagination_range"]

            content = response.content.decode("utf-8")
            content_2 = response_2.content.decode("utf-8")
            content_3 = response_3.content.decode("utf-8")

            self.assertEqual(context["page_range"], range(1, 7))
            self.assertEqual(context["current_page"], 1)
            self.assertEqual(context["stop_range"], 5)
            self.assertIn(
                '<spam class="page-link page-item current-page">1</spam>',
                content
            )

            self.assertEqual(context_2["page_range"], range(1, 7))
            self.assertEqual(context_2["current_page"], 3)
            self.assertEqual(context_2["stop_range"], 5)
            self.assertIn(
                '<spam class="page-link page-item current-page">3</spam>',
                content_2
            )

            self.assertEqual(context_3["page_range"], range(1, 7))
            self.assertEqual(context_3["current_page"], 4)
            self.assertEqual(context_3["stop_range"], 6)
            self.assertIn(
                '<spam class="page-link page-item current-page">4</spam>',
                content_3
            )

    def test_recipe_list_items_per_page_is_correct(self):
        self.make_multiples_recipes(10)
        with patch("recipes.views.ITEMS_PER_PAGE", new=3):
            response = self.client.get(reverse("recipes:list"))
            recipes = response.context["recipes"]
            paginator = recipes.paginator

            self.assertEqual(paginator.num_pages, 4)
            self.assertEqual(len(paginator.get_page(1)), 3)
            self.assertEqual(len(paginator.get_page(2)), 3)
            self.assertEqual(len(paginator.get_page(3)), 3)
            self.assertEqual(len(paginator.get_page(4)), 1)

    def test_invalid_page_query_uses_page_one(self):
        response = self.client.get(reverse("recipes:list") + "?page=abc")
        current_page = response.context["pagination_range"]["current_page"]
        self.assertEqual(current_page, 1)
