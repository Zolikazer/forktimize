import { render, screen } from "@testing-library/svelte";
import { describe, expect, test, vi } from "vitest";
import Menu from "$lib/components/menu/Menu.svelte";

// Mock the Food component
// vi.mock("$lib/components/menu/Food.svelte", () => ({
//   default: vi.fn().mockImplementation(() => ({
//     $$render: () => '<div class="mocked-food"></div>',
//     $$slot_def: {},
//     $set: () => {}
//   }))
// }));

// Mock the menu store
vi.mock("$lib/stores/menuStore.js", () => {
  const mockMenu = [
    {
      name: "Test Food 1",
      calories: 300,
      protein: 20,
      carbs: 40,
      fats: 10,
      price: 1500
    },
    {
      name: "Test Food 2",
      calories: 400,
      protein: 25,
      carbs: 50,
      fats: 15,
      price: 2000
    }
  ];

  return {
    menu: {
      subscribe: vi.fn().mockImplementation((run) => {
        run(mockMenu);
        return { unsubscribe: vi.fn() };
      })
    }
  };
});

describe("Menu Component", () => {
  test("renders title correctly", () => {
    render(Menu);
    expect(screen.getByText("Your Menu For Wednesday")).toBeInTheDocument();
  });

  test("renders a Food component for each item in the menu", () => {
    const { container } = render(Menu);
    const foodComponents = container.querySelectorAll('.food-card');
    expect(foodComponents.length).toBe(2);
  });
});
