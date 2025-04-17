import Blockly from 'blockly';

// PyQUBO Variable Block - Enhanced with all variable types
Blockly.Blocks['pyqubo_variable'] = {
  init: function() {
    this.jsonInit({
      "type": "pyqubo_variable",
      "message0": "Create %1 variable %2",
      "args0": [
        {
          "type": "field_dropdown",
          "name": "TYPE",
          "options": [
            ["Binary", "Binary"],
            ["Spin", "Spin"], 
            ["Integer", "Integer"]
          ]
        },
        {
          "type": "field_input",
          "name": "NAME",
          "text": ""
        }
      ],
      "previousStatement": null,
      "nextStatement": null,
      "colour": 230,
      "tooltip": "Define a PyQUBO variable",
      "helpUrl": ""
    });
  }
};

// Modified Array Variable Block to properly handle complex shapes
Blockly.Blocks['pyqubo_array_variable'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Create Array")
        .appendField(new Blockly.FieldTextInput(""), "NAME");
    this.appendDummyInput()
        .appendField("shape:");
    this.appendValueInput("SHAPE")
        .setCheck(["Array", "Number"]);  // Accept both array and number inputs
    this.appendDummyInput()
        .appendField("vartype:")
        .appendField(new Blockly.FieldDropdown([
            ["Binary", "Binary"],
            ["Spin", "Spin"]
        ]), "VARTYPE");
    this.setInputsInline(true);  // This makes the block more compact
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(230);
    this.setTooltip("Create an array variable for PyQUBO with sequential numbering");
  }
};

// New Array Shape Input Block for 2D arrays
Blockly.Blocks['array_shape_input'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("[")
        .appendField(new Blockly.FieldNumber(3, 1, 100), "ROWS")
        .appendField(",")
        .appendField(new Blockly.FieldNumber(3, 1, 100), "COLS")
        .appendField("]");
    this.setOutput(true, "Array");
    this.setColour(230);
    this.setTooltip("Define a 2D array shape with rows and columns");
  }
};

// PyQUBO Constraint Block
Blockly.Blocks['pyqubo_constraint'] = {
  init: function() {
    this.appendValueInput("LHS")
        .setCheck(["String", "Number", "Boolean"])
        .appendField("Add constraint:");
    this.appendDummyInput()
        .appendField(new Blockly.FieldDropdown([
            ["=", "="],
            ["<=", "<="],
            [">=", ">="],
            ["!=", "!="]
        ]), "OPERATOR");
    this.appendValueInput("RHS")
        .setCheck(["String", "Number", "Boolean"]);
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(230);
    this.setTooltip("Add a constraint to the QUBO model");
  }
};

// PyQUBO Objective Block
Blockly.Blocks['pyqubo_objective'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Set objective to")
        .appendField(new Blockly.FieldDropdown([
            ["maximize", "maximize"],
            ["minimize", "minimize"]
        ]), "GOAL");
    this.appendValueInput("EXPRESSION")
        .setCheck(["String", "Number", "Boolean"]);
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(230);
    this.setTooltip("Define the objective function to optimize");
  }
};

// PyQUBO Expression Block
Blockly.Blocks['pyqubo_expression'] = {
  init: function() {
    this.jsonInit({
      "type": "pyqubo_expression",
      "message0": "%1 %2 %3",
      "args0": [
        {
          "type": "input_value",
          "name": "LEFT",
          "check": ["String", "Number", "Boolean", "Variable"]
        },
        {
          "type": "field_dropdown",
          "name": "OPERATOR",
          "options": [
            ["+", "+"],
            ["-", "-"],
            ["*", "*"],
            ["/", "/"],
            ["^", "**"]
          ]
        },
        {
          "type": "input_value",
          "name": "RIGHT",
          "check": ["String", "Number", "Boolean", "Variable"]
        }
      ],
      "output": ["String", "Number"],
      "colour": 230,
      "tooltip": "Create a mathematical expression",
      "helpUrl": ""
    });
  }
};

// Variable Reference Block
Blockly.Blocks['pyqubo_var_reference'] = {
  init: function() {
    this.jsonInit({
      "type": "pyqubo_var_reference",
      "message0": "variable %1",
      "args0": [
        {
          "type": "field_input",
          "name": "NAME",
          "text": ""
        }
      ],
      "output": ["String", "Number"],
      "colour": 230,
      "tooltip": "Reference a variable in an expression",
      "helpUrl": ""
    });
  }
};

// Updated Array Reference Block
Blockly.Blocks['pyqubo_array_reference'] = {
  init: function() {
    this.jsonInit({
      "type": "pyqubo_array_reference",
      "message0": "array %1 [ %2 ]",
      "args0": [
        {
          "type": "field_input",
          "name": "NAME",
          "text": ""
        },
        {
          "type": "input_value",
          "name": "INDEX",
          "check": "Number"
        }
      ],
      "output": ["String", "Number"],
      "colour": 230,
      "tooltip": "Reference an array element in an expression",
      "helpUrl": ""
    });
  }
};

// Sum of Array Elements Block
Blockly.Blocks['pyqubo_array_sum'] = {
  init: function() {
    this.jsonInit({
      "type": "pyqubo_array_sum",
      "message0": "sum of array %1 from %2 to %3",
      "args0": [
        {
          "type": "field_input",
          "name": "NAME",
          "text": ""
        },
        {
          "type": "input_value",
          "name": "FROM",
          "check": "Number"
        },
        {
          "type": "input_value",
          "name": "TO",
          "check": "Number"
        }
      ],
      "output": ["String", "Number"],
      "colour": 230,
      "tooltip": "Calculate the sum of array elements",
      "helpUrl": ""
    });
  }
};

// PyQUBO Model Function - The main container for a QUBO model
Blockly.Blocks['pyqubo_model'] = {
  init: function() {
    this.jsonInit({
      "type": "pyqubo_model",
      "message0": "QUBO Model %1 For function: %2",
      "args0": [
        {
          "type": "input_dummy"
        },
        {
          "type": "field_input",
          "name": "NAME",
          "text": "createQuboForSingleMove"
        }
      ],
      "message1": "Variables %1",
      "args1": [
        {
          "type": "input_statement",
          "name": "VARIABLES",
          "check": null
        }
      ],
      "message2": "Constraints %1",
      "args2": [
        {
          "type": "input_statement",
          "name": "CONSTRAINTS",
          "check": null
        }
      ],
      "message3": "Objective %1",
      "args3": [
        {
          "type": "input_statement",
          "name": "OBJECTIVE",
          "check": null
        }
      ],
      "colour": 230,
      "tooltip": "Create a complete QUBO model",
      "helpUrl": ""
    });
  }
};

// This keeps backward compatibility with the original PyQUBO function block
Blockly.Blocks['pyqubo_function'] = {
  init: function() {
    this.jsonInit({
      "type": "pyqubo_function",
      "message0": "Define function %1 with parameter %2",
      "args0": [
        {
          "type": "field_input",
          "name": "NAME",
          "text": ""
        },
        {
          "type": "input_value",
          "name": "PARAM"
        }
      ],
      "message1": "Variables, Constraints, and Objective %1",
      "args1": [
        {
          "type": "input_statement",
          "name": "BODY"
        }
      ],
      "colour": 230,
      "tooltip": "Define a function that returns a PyQUBO model",
      "helpUrl": ""
    });
  }
};

// QUBO Result Display Block
Blockly.Blocks['pyqubo_result_display'] = {
  init: function() {
    this.jsonInit({
      "type": "pyqubo_result_display",
      "message0": "Display QUBO results",
      "colour": 230,
      "tooltip": "Display the results of the QUBO computation showing the optimal solution",
      "helpUrl": "",
      "previousStatement": null,
      "nextStatement": null
    });
  }
};

// Raw text block for expressions without quotes
Blockly.Blocks['raw_text'] = {
  init: function() {
    this.jsonInit({
      "type": "raw_text",
      "message0": "raw text %1",
      "args0": [
        {
          "type": "field_input",
          "name": "TEXT",
          "text": "" 
        }
      ],
      "output": ["String", "Number"],
      "colour": 160,
      "tooltip": "Text without quotes for expressions",
      "helpUrl": ""
    });
  }
};

export default {
  blocks: [
    'pyqubo_variable',
    'pyqubo_array_variable',
    'array_shape_input',
    'pyqubo_constraint',
    'pyqubo_objective',
    'pyqubo_expression',
    'pyqubo_var_reference',
    'pyqubo_array_reference',
    'pyqubo_array_sum',
    'pyqubo_model',
    'pyqubo_function',
    'pyqubo_result_display',
    'raw_text'
  ]
};