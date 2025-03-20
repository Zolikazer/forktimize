import {fireEvent, render, screen} from "@testing-library/svelte";
import {beforeEach, describe, expect, test} from "vitest";
import {errorStore} from "$lib/stores/errorStore.js";
import {get} from "svelte/store";
import ErrorDialog from "$lib/components/help/ErrorDialog.svelte";

beforeEach(() => {
    errorStore.set({show: false, message: ""});
});

describe("ErrorDialog Component", () => {
    test("does not render when no error is present", () => {
        render(ErrorDialog);
        expect(screen.queryByText(/Error 😱/)).not.toBeInTheDocument();
    });

    test("renders the error message when errorStore.show is true", async () => {
        errorStore.set({show: true, message: "Something went wrong!"});
        render(ErrorDialog);

        expect(screen.getByText(/Error 😱/)).toBeInTheDocument();
        expect(screen.getByText("Something went wrong!")).toBeInTheDocument();
        expect(screen.getByText(/Try again later!/)).toBeInTheDocument();
    });
});
