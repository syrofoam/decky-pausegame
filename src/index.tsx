import {
  ButtonItem,
  definePlugin,
  ServerAPI,
} from "decky-frontend-lib";
import { FaPause } from "react-icons/fa";

export default definePlugin((serverApi: ServerAPI) => {
  return {
    title: <div style={{ fontWeight: "bold" }}>Quick Pause</div>,
    content: (
      <ButtonItem
        layout="below"
        onClick={async () => {
           await serverApi.callPluginMethod("toggle_game", {});
        }}
      >
        <FaPause /> Toggle Pause/Resume
      </ButtonItem>
    ),
    icon: <FaPause />,
  };
});
