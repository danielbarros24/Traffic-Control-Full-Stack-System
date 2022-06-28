import Rete from "rete";
import * as Socket from "../../sockets";
import Node from "../../../../node_modules/rete-vue-render-plugin/src/logical-operators/Node.vue";

export class NOTComponent extends Rete.Component {
    constructor(){
        super("NOT");
        this.data.component = Node;
    }
    
    builder(node) {
        var inp1 = new Rete.Input('input1',"In", Socket.boolean);
        var out = new Rete.Output('num', "Out", Socket.boolean);

        return node
            .addInput(inp1)
            .addOutput(out);
    }
    
    worker(node, inputs, outputs) {
        outputs['num'] = node.data.input;
    }

    _inputToJsonLogic(node, name) {
        const { inputs } = node;

        const input = inputs.get(name)
        const { connections } = input;

        if (connections.length == 0) {
            return {};
        }

        const connection = connections[0];
        const connectionNode = connection.output.node;
        const connectionComponent = this.editor.getComponent(connectionNode.name);

        return connectionComponent.toJsonLogic?.(connectionNode);
    }

    toJsonLogic(node) {
        const input1 = this._inputToJsonLogic(node, 'input1')

        return {"!" : input1}
    }
    
}