import Blockly from 'blockly';

// Define a new block for raw text (without quotes)
Blockly.Blocks['raw_text'] = {
  init: function() {
    this.jsonInit({
      "type": "raw_text",
      "message0": "raw text %1",
      "args0": [
        {
          "type": "field_input",
          "name": "TEXT",
          "text": "" // Empty by default
        }
      ],
      "output": "String",
      "colour": 160,
      "tooltip": "Text without quotes for expressions",
      "helpUrl": ""
    });
  }
};

export default Blockly.Blocks['raw_text'];