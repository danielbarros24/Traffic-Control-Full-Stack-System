import Rete from "rete";
import * as Socket from "../../sockets";
import Node from "../../../../node_modules/rete-vue-render-plugin/src/logical-operators/Node.vue";


export class LessThanOrEqualToComponent extends Rete.Component {
    constructor(){
        super("A<=B");
        this.data.component = Node;
    }
    
    builder(node) {
        var inp1 = new Rete.Input('input1',"A", Socket.number);
        var inp2 = new Rete.Input('input2',"B", Socket.number);
        var out = new Rete.Output('num', "Out", Socket.boolean);

        return node
            .addInput(inp1)
            .addInput(inp2)
            .addOutput(out);
    }
    
    worker(node, inputs,  outputs) {
        outputs['num'] = node.data.num;
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
        const json1 = this._inputToJsonLogic(node, 'input1')
        const json2 = this._inputToJsonLogic(node, 'input2')

        return {"<=" : [json1, json2]}
    }
}