import Rete from "rete";
import * as Socket from "../sockets";

export class LessThanComponent extends Rete.Component {
    constructor(){
        super("<");
    }
    
    builder(node) {
        var inp1 = new Rete.Input('num1',"In1", Socket.number);
        var inp2 = new Rete.Input('num2',"In2", Socket.number);
        var out = new Rete.Output('num', "Out", Socket.number);
        return node
            .addInput(inp1)
            .addInput(inp2)
            .addOutput(out);
    }
    
    worker(node, inputs, outputs) {
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
        const json1 = this._inputToJsonLogic(node, 'num1')
        const json2 = this._inputToJsonLogic(node, 'num2')

        return {">" : [json1, json2]}
    }
}