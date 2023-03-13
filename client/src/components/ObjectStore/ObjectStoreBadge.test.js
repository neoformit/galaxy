import { mount } from "@vue/test-utils";
import { getLocalVue } from "tests/jest/helpers";
import ObjectStoreBadge from "./ObjectStoreBadge";
import { ROOT_COMPONENT } from "utils/navigation";

const localVue = getLocalVue(true);

const TEST_MESSAGE = "a test message provided by backend";

describe("ObjectStoreBadge", () => {
    let wrapper;

    function mountBadge(badge) {
        wrapper = mount(ObjectStoreBadge, {
            propsData: { badge },
            localVue,
            stubs: { "b-popover": true },
        });
    }

    it("should render a valid badge for more_secure type", async () => {
        mountBadge({ type: "more_secure", message: TEST_MESSAGE });
        const selector = ROOT_COMPONENT.object_store_details.badge_of_type({ type: "more_secure" }).selector;
        const iconEl = wrapper.find(selector);
        expect(iconEl.exists()).toBeTruthy();
        expect(wrapper.vm.message).toContain(TEST_MESSAGE);
        expect(wrapper.vm.stockMessage).toContain("more secure by the Galaxy adminstrator");
    });

    it("should render a valid badge for less_secure type", async () => {
        mountBadge({ type: "less_secure", message: TEST_MESSAGE });
        const selector = ROOT_COMPONENT.object_store_details.badge_of_type({ type: "less_secure" }).selector;
        const iconEl = wrapper.find(selector);
        expect(iconEl.exists()).toBeTruthy();
        expect(wrapper.vm.message).toContain(TEST_MESSAGE);
        expect(wrapper.vm.stockMessage).toContain("less secure by the Galaxy adminstrator");
    });
});
