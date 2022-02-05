import App from "../App";
import withMock from "storybook-addon-mock";

export default {
  title: "App",
  component: App,
  decorators: [withMock],
};

const Template = () => <App />;

export const Default = Template.bind({});

// @ts-ignore
Default.parameters = {
  mockData: [
    {
      url: "/api/status/all",
      method: "GET",
      status: 200,
      response: [
        { connected: false, name: "Test 1", state: null },
        { connected: true, name: "Test 2", state: "busy" },
        { connected: true, name: "Test 4", state: "off" },
      ],
    },
  ],
};
