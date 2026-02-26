import {
  ButtonItem,
  definePlugin,
  ServerAPI,
  Static,
} from "decky-frontend-lib";
import { FaPause } from "react-icons/fa";

export default definePlugin((serverApi: ServerAPI) => {
  return {
    title: <div className={Static.Title}>Quick Pause</div>,
    content: (
      <ButtonItem
        layout="below"
        onClick={async () => {
           // We just call "toggle_game" and let Python figure out the rest
           await serverApi.callPluginMethod("toggle_game", {});
        }}
      >
        <FaPause /> Toggle Pause/Resume
      </ButtonItem>
    ),
    icon: <FaPause />,
  };
});
