import Rete from "rete";
import * as Socket from "../sockets";

import Node from "rete-vue-render-plugin/src/end/Node.vue";
import { SelectControl } from "@/node-editor/controls/SelectControl/SelectControl";
import { SwitchControl } from "@/node-editor/controls/SwitchControl/SwitchControl";

export class GpioComponent extends Rete.Component {
    constructor(){
        super("GPIO");
        this.data.component = Node;
    }

    async builder(node) {
      const responseGpios = await fetch("http://127.0.0.1:5000/pins");
      const jsonGpios = await responseGpios.json();

      
        var input = new Rete.Input('num', "Input", Socket.boolean, true);
        return node
          .addInput(input)
          .addControl(new SelectControl(this.editor, 'type1', jsonGpios.map((value) => ({
            text: `GPIO ${value}`, value: value,
          })), "GPIO"))
          .addControl(new SwitchControl(this.editor, 'type'))
    }

    worker(node, inputs, outputs) {
    }

    toJsonLogic(node) {
        const { inputs } = node;

        if (inputs.length == 0) {
            return {};
        }

        const inputNum = inputs.get('num')
        const { connections } = inputNum;

        if (connections.length == 0) {
            return {};
        }

        const connection = connections[0];
        const connectionNode = connection.output.node;
        const connectionComponent = this.editor.getComponent(connectionNode.name);

        return connectionComponent.toJsonLogic?.(connectionNode);
    }

    toGPIO(node) {
        const gpio = parseInt(node.data.type1)
        const inverted = node.data.type

        return {gpio, inverted}
    }
}