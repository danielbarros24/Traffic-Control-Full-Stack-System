<template>
  <div>
    <div class="wrapper"><div class="node-editor" ref="nodeEditor"></div></div>
    <canvas id="canvasOutput"></canvas>
  </div>
</template>

<script>
import { Socket, NodeEditor, Control, Output, Input, Component, Engine } from "rete";

import ConnectionPlugin from "rete-connection-plugin";
import VueRenderPlugin from "rete-vue-render-plugin";
import ContextMenuPlugin from "rete-context-menu-plugin";
import AreaPlugin from "rete-area-plugin";
import KeyboardPlugin from 'rete-keyboard-plugin';

import ReteNumControl from './ReteNumControl'

export default {
  data() {
    return {
      editor: null
    };
  },

  async mounted() {
    var numSocket = new Socket('num');
    var vehileSocket = new Socket('Vehicle');
    var roadSocket = new Socket('Road');

    class NumControl extends Control {
      constructor(emitter, key, readonly) {
        super(key);
        
        this.component = ReteNumControl;
        this.props = { emitter, ikey: key, readonly };
      }

      setValue(val) {
        this.vueContext.value = val;
      }
    }

    class ConstantComponent extends Component {
        constructor(){
            super("Constante");
        }

        builder(node) {
            var out1 = new Output('num', "number", numSocket);
            return node
              .addControl(new NumControl(this.editor, 'num'))
              .addOutput(out1);
        }

        worker(node, inputs, outputs) {
            outputs['num'] = node.data.num;
        }
    }

    class TempoDePermanenciaComponent extends Component {
        constructor(){
            super("Tempo de permanência");
        }

        builder(node) {
            var inp1 = new Input('str', "Vehicle", vehileSocket);
            var inp2 = new Input('num', "In", numSocket);
            var out = new Output('num', "Out", numSocket);

            return node

                .addInput(inp2)
                .addInput(inp1)
                .addControl(new NumControl(this.editor, 'num'))
                .addOutput(out);
        }

        worker(node, outputs) {
            outputs['num'] = node.data.num;
        }
    }

    class FluxoComponent extends Component {
        constructor(){
            super("Fluxo");
        }

        builder(node) {

            var inp1 = new Input('str', "Number of vehicles", vehileSocket);
            var inp2 = new Input('num', "In", numSocket);

            var inp3 = new Input('num', "temp", numSocket);
            var out1 = new Output('Out', "Out", numSocket);

            return node

              .addInput(inp2)
              .addInput(inp1)
              .addInput(inp3)
              .addOutput(out1);
        }

        worker(node, outputs) {
            outputs['num'] = node.data.num;
        }
    }

    class NumeroDeVeiculosComponent extends Component {
        constructor(){
            super("Número de veículos");
        }

        builder(node) {
            var out1 = new Output('num', "Number", numSocket);
            return node
              .addControl(new NumControl(this.editor, 'num'))
              .addOutput(out1);
        }

        worker(node, inputs, outputs) {
            outputs['num'] = node.data.num;
        }
    }

    class FilaComponent extends Component {
        constructor(){
            super("Fila");
        }

        builder(node) {
            var out1 = new Output('num', "Number", numSocket);
            return node
              .addControl(new NumControl(this.editor, 'num'))
              .addOutput(out1);
        }

        worker(node, inputs, outputs) {
            outputs['num'] = node.data.num;
        }
    }

    class AddComponent extends Component {
        constructor(){
            super("+");
        }
        
        builder(node) {
            var inp1 = new Input('num',"Number", numSocket, true);
            var out = new Output('num', "Number", numSocket);

            return node
                .addInput(inp1)
                .addControl(new NumControl(this.editor, 'preview', true))
                .addOutput(out);
        }
        
        worker(node, inputs, outputs) {
            var sum = inputs['num'].reduce((partialSum, a) => partialSum + a, 0);
            this.editor.nodes.find(n => n.id == node.id).controls.get('preview').setValue(sum);
            outputs['num'] = sum;
        }
    }

    class MultiplyComponent extends Component {
        constructor(){
            super("x");
        }
        
        builder(node) {
            var inp1 = new Input('num',"Number", numSocket, true);
            var out = new Output('num', "Number", numSocket);

            return node
                .addInput(inp1)
                .addControl(new NumControl(this.editor, 'preview', true))
                .addOutput(out);
        }
        
        worker(node, inputs, outputs) {
            var sum = inputs['num'].reduce((partialSum, a) =>  partialSum * a, 1);
            this.editor.nodes.find(n => n.id == node.id).controls.get('preview').setValue(sum);
            outputs['num'] = sum;
        }
    }

    class DivisionComponent extends Component {
        constructor(){
            super("/");
        }
        
        builder(node) {
            var inp1 = new Input('num',"Number", numSocket, true);
            var out = new Output('num', "Number", numSocket);

            return node
                .addInput(inp1)
                .addControl(new NumControl(this.editor, 'preview', true))
                .addOutput(out);
        }
        
        worker(node, inputs, outputs) {
            var sum = inputs['num'].reduce((partialSum, a) =>  partialSum / a, 1);
            this.editor.nodes.find(n => n.id == node.id).controls.get('preview').setValue(sum);
            outputs['num'] = sum;
        }
    }

    class EqualToComponent extends Component {
        constructor(){
            super("=");
        }
        
        builder(node) {
            var inp1 = new Input('num',"Number", numSocket, true);
            var out = new Output('num', "Number", numSocket);

            return node
                .addInput(inp1)
                .addOutput(out);
        }
        
        worker(node, inputs, outputs) {
            var sum = inputs['num'].reduce((partialSum, a) =>  partialSum / a, 1);
            this.editor.nodes.find(n => n.id == node.id).controls.get('preview').setValue(sum);
            outputs['num'] = sum;
        }
    }

    class DifferentThanComponent extends Component {
        constructor(){
            super("!=");
        }
        
        builder(node) {
            var inp1 = new Input('num',"Number", numSocket, true);
            var out = new Output('num', "Number", numSocket);

            return node
                .addInput(inp1)
                .addOutput(out);
        }
        
        worker(node, inputs, outputs) {
            var sum = inputs['num'].reduce((partialSum, a) =>  partialSum / a, 1);
            this.editor.nodes.find(n => n.id == node.id).controls.get('preview').setValue(sum);
            outputs['num'] = sum;
        }
    }

    class GreaterThanComponent extends Component {
        constructor(){
            super(">");
        }
        
        builder(node) {
            var inp1 = new Input('num',"Number", numSocket, true);
            var out = new Output('num', "Number", numSocket);

            return node
                .addInput(inp1)
                .addOutput(out);
        }
        
        worker(node, inputs, outputs) {
            var sum = inputs['num'].reduce((partialSum, a) =>  partialSum / a, 1);
            this.editor.nodes.find(n => n.id == node.id).controls.get('preview').setValue(sum);
            outputs['num'] = sum;
        }
    }

    class LessThanComponent extends Component {
        constructor(){
            super("<");
        }
        
        builder(node) {
            var inp1 = new Input('num',"Number", numSocket, true);
            var out = new Output('num', "Number", numSocket);

            return node
                .addInput(inp1)
                .addOutput(out);
        }
        
        worker(node, inputs, outputs) {
            var sum = inputs['num'].reduce((partialSum, a) =>  partialSum / a, 1);
            this.editor.nodes.find(n => n.id == node.id).controls.get('preview').setValue(sum);
            outputs['num'] = sum;
        }
    }

    class GreaterThanOrEqualToComponent extends Component {
        constructor(){
            super(">=");
        }
        
        builder(node) {
            var inp1 = new Input('num',"Number", numSocket, true);
            var out = new Output('num', "Number", numSocket);

            return node
                .addInput(inp1)
                .addOutput(out);
        }
        
        worker(node, inputs, outputs) {
            var sum = inputs['num'].reduce((partialSum, a) =>  partialSum / a, 1);
            this.editor.nodes.find(n => n.id == node.id).controls.get('preview').setValue(sum);
            outputs['num'] = sum;
        }
    }

    class LessThanOrEqualToComponent extends Component {
        constructor(){
            super("<=");
        }
        
        builder(node) {
            var inp1 = new Input('num',"Number", numSocket, true);
            var out = new Output('num', "Number", numSocket);

            return node
                .addInput(inp1)
                .addOutput(out);
        }
        
        worker(node, inputs, outputs) {
            var sum = inputs['num'].reduce((partialSum, a) =>  partialSum / a, 1);
            this.editor.nodes.find(n => n.id == node.id).controls.get('preview').setValue(sum);
            outputs['num'] = sum;
        }
    }

    class ANDComponent extends Component {
        constructor(){
            super("AND");
        }
        
        builder(node) {
            var inp1 = new Input('num',"Number", numSocket, true);
            var out = new Output('num', "Number", numSocket);

            return node
                .addInput(inp1)
                .addOutput(out);
        }
        
        worker(node, inputs, outputs) {
            var sum = inputs['num'].reduce((partialSum, a) =>  partialSum / a, 1);
            this.editor.nodes.find(n => n.id == node.id).controls.get('preview').setValue(sum);
            outputs['num'] = sum;
        }
    }

    class ORComponent extends Component {
        constructor(){
            super("OR");
        }
        
        builder(node) {
            var inp1 = new Input('num',"Number", numSocket, true);
            var out = new Output('num', "Number", numSocket);

            return node
                .addInput(inp1)
                .addOutput(out);
        }
        
        worker(node, inputs, outputs) {
            var sum = inputs['num'].reduce((partialSum, a) =>  partialSum / a, 1);
            this.editor.nodes.find(n => n.id == node.id).controls.get('preview').setValue(sum);
            outputs['num'] = sum;
        }
    }

    class NOTComponent extends Component {
        constructor(){
            super("NOT");
        }
        
        builder(node) {
            var inp1 = new Input('num',"Number", numSocket, true);
            var out = new Output('num', "Number", numSocket);

            return node
                .addInput(inp1)
                .addOutput(out);
        }
        
        worker(node, inputs, outputs) {
            var sum = inputs['num'].reduce((partialSum, a) =>  partialSum / a, 1);
            this.editor.nodes.find(n => n.id == node.id).controls.get('preview').setValue(sum);
            outputs['num'] = sum;
        }
    }
    

    var container = this.$refs.nodeEditor
    var components = [new ConstantComponent(), new TempoDePermanenciaComponent(), new FluxoComponent(), new NumeroDeVeiculosComponent(), 
      new FilaComponent(), new AddComponent(), new MultiplyComponent(), new DivisionComponent(), new EqualToComponent(), 
      new DifferentThanComponent(), new GreaterThanComponent(), new LessThanComponent(), new GreaterThanOrEqualToComponent(), new LessThanOrEqualToComponent(), 
      new ANDComponent(), new ORComponent(), new NOTComponent()];
    var editor = new NodeEditor('demo@0.1.0', container);

    editor.use(ConnectionPlugin);
    editor.use(VueRenderPlugin);
    editor.use(ContextMenuPlugin);
    editor.use(AreaPlugin);
    editor.use(KeyboardPlugin);

    var engine = new Engine('demo@0.1.0');
    components.map(c => {
        editor.register(c);
        engine.register(c);
    });

    var n1 = await components[0].createNode({num: 2});
    var n2 = await components[0].createNode({num: 0});
    var add = await components[1].createNode();
    var sub = await components[2].createNode();
    

    n1.position = [80, 200];
    n2.position = [80, 400];
    add.position = [500, 240];
    sub.position = [800, 240];

    editor.on('process nodecreated noderemoved connectioncreated connectionremoved', async () => {
      console.log('process');
        await engine.abort();
        await engine.process(editor.toJSON());
        console.log(editor.toJSON())
    });
    
    editor.view.resize();
    AreaPlugin.zoomAt(editor);
    editor.trigger('process');
  }
};
</script>

<style>
.node-editor {
  text-align: left;
  overflow: hidden;
}
.node .control input, .node .input-control input {
  width: 140px;
}
select, input {
  width: 100%;
  border-radius: 30px;
  background-color: white;
  padding: 2px 6px;
  border: 1px solid #999;
  font-size: 110%;
  width: 170px;
}
</style>