import Archive from "./Archive.vue";
import { mountWithDetails } from "./testHelpers";

describe("Archive.vue", () => {
    it("loads with correct initial state", async () => {
        const { wrapper } = mountWithDetails(Archive);
        expect(wrapper.vm.showHelper).toBe(true);
        expect(wrapper.find("#btn-reset").classes()).toEqual(expect.arrayContaining(["disabled"]));
        expect(wrapper.find("#btn-start").classes()).toEqual(expect.arrayContaining(["disabled"]));
        expect(wrapper.find("#btn-stop").classes()).toEqual(expect.arrayContaining(["disabled"]));
        expect(wrapper.findAll(".ui-limitloader").length).toBe(0);
    });
});
