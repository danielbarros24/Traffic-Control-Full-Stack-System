import Rete from "rete";
import * as Socket from "../sockets";

export class EndComponent extends Rete.Component {
    constructor(){
        super("End");
    }

    builder(node) {
        var input = new Rete.Input('num', "Input", Socket.number);
        return node
          .addInput(input);
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
}