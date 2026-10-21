# PDH Academy

# Piping and Instrumentation Diagrams

by

Mark Ludwigson, P.E., PMP

Course 462 4 PDH (4 Hours)

PO Box 449

Pewaukee, WI 53072

(888) 564 - 9098

support@pdhacademy.com

# Piping and Instrumentation Diagrams

Course Outline:

Overview of P&IDs

Other Types of Diagrams

Industry Standards

Letter Designations

Symbols

Control Loops

Helpful References

Examination

# Piping and Instrumentation Diagrams

## Overview of P&IDs

Piping and Instrumentation Diagrams (P&IDs) are drawings showing piping and communications as schematic (unscaled) lines and control features as symbols. P&IDs illustrate the functional relationship of piping, instrumentation, equipment, and controllers. They are usually located in the instrumentation drawings in a project drawing set. P&IDs are commonly made by process engineers, controls engineers, and electrical engineers.

The main purpose of a P&ID is to indicate if devices are automatically controlled, and if so, how they are interlocked with instruments. P&IDs convey the interconnectivity of automated components. See Figure 1 for an example in which there is interconnectivity between a pump (P-4-3) and a solenoid valve (FV-4-3) for controlling seal water to the mechanical seals on the pump. To conserve water, the seal water should only flow when the pump is operating. The wiring from the motor starter (MS) to the solenoid (S) allows for the automated control of the seal water.

![](images/de8c9022d6a56732522444a7d789cbf2aeb794b23ba3be72fb09d2f1f5f37c94.jpg)  
Figure 1: Example P&ID for a pump and a valve.

For Figure 1, the control description is as follows: Valve FV-4-3 shall open when pump P-4-3 turns on. Valve FV-4-3 shall close when pump P-4-3 turns off.

# Piping and Instrumentation Diagrams

P&IDs are helpful for the following reasons, organized by project phase:

## • Design:

o Helps coordinate instrumentation, controls, and wiring details between process engineers, controls engineers, and electrical engineers.

o Helps to create detailed control descriptions and control loops.

o Used to develop Hazard and Operability Studies (HAZOP).

## • Procurement:

o Specifies instrumentation and controls details needed for obtaining quotes.

o Provides control details needed for estimating programming costs.

## • Construction:

o Specifies details needed for purchasing and installing instruments, electrical devices, and controls components.

o Provides details needed for the programming of controllers.

o Helps confirm that communication wires have been terminated correctly.

o Field changes can be easily recorded on as-built drawings.

o Utilized during startup and training to understand the function of the system or process.

## • Operation:

o As-built P&IDs provide control details needed for making operation decisions.

o P&ID format is easy to understand compared to programing code or written descriptions.

o Operators can read the P&IDs and understand operations options.

o Helpful for a Job Hazard Analysis (JHA).

o Helps when preparing for system modifications as part of Management of Change (MOC).

# Piping and Instrumentation Diagrams

Typical steps to create a P&ID are as follows:

1. Block flow diagram is created.

2. Process flow diagram (PFD) is created.

3. High-level control descriptions are written.

4. Draft P&IDs are created using process flow diagrams as backgrounds.

5. Areas are drawn at the top of P&IDs for controllers, MCCs (motor control centers), and/or SCADA (supervisory control and data acquisition).

6. Symbols and labels are added to P&IDs for control features.

7. Wiring is drawn on P&IDs to connect electrical devices with controllers, MCCs, and/or SCADA.

8. Detailed control descriptions are completed.

9. Control loops are defined, typically in a table format.

10. Identification numbers on P&IDs are matched with control descriptions and control loops.

11.Quality review performed and corrections made.

## Other Types of Diagrams

Piping and Instrumentation Diagrams are also called Process and Instrumentation Diagrams since the focus is more on the process than the piping. Both are referred to as P&IDs. P&IDs are related to the following other types of engineering diagrams.

## Block Flow Diagram

In the planning stage or early in design, a block flow diagram is commonly made by a process engineer. Block flow diagrams show the main processes as rectangles or circles with lines and arrows for the main flow paths. See Figure 2 for an example of a block flow diagram for a water treatment system.

![](images/0ceadc2660edce3a77c80e65c5f71f1c38899726ff895b00c85bb00c0835c3b3.jpg)  
Figure 2: Example of a block flow diagram  
Source: “Arsenic Removal from Drinking Water by Ion Exchange and Activated Alumina Plants”, EPA 600/R-00/088

# Piping and Instrumentation Diagrams

## Process Flow Diagram

Process flow diagrams (PFDs) are created by process or mechanical engineers early in the design stage. A PFD is a drawing with lines for piping and symbols for major components such as pumps, tanks, mixers, and flow meters. Ideally, all major components should be identified, including instrumentation. See Figures 3 and 4 for examples.

PFDs are often given to electrical and controls engineers to create P&IDs. PFDs are often used as the background in CAD for creating the P&IDs. Control and communication details are added to the PFD backgrounds to make P&IDs.

![](images/f46d8df97a3b321af5cd0eba439de5aa76957e273d0ef1612682622bced55495.jpg)  
Figure 3: Example PFD with basic features. This drawing could be a starting point for creating a P&ID with control and communication details.  
Source: www.epa.gov/sites/default/files/2019-07/documents/wbs-ixclo4-documentation-june-2019.pdf (public domain)

![](images/f88630c47cc218f9c44470d57791f5cb694772b6f134abef8a8778aa5d3d73de.jpg)  
Figure 4: Example PFD with details such as pipe size, fluid type and motorized/automated valves shown with an “M” in a box.

It is common for a legend drawing to be included with a drawing set to define the symbols, abbreviations, line types, shading, etc., utilized on the PFDs and P&IDs. Sometimes there are common legend drawings and sometimes there are separate legend drawings for PFDs and P&IDs.

# Piping and Instrumentation Diagrams

## Instrument Schematic

Instrument schematics (or diagrams) are detailed drawings for particular instruments. They show wiring details with some control logic notes that pertain only to that instrument. See Figure 5 for an example. Instrument schematics differ from a P&ID which shows the interconnectivity of various instruments, equipment, and panels.

![](images/c71cf9bbbd0ce049963d0126e55cdda5bc925a48568566e495e0539333b7e40c.jpg)  
Figure 5: Example instrument schematic for a flow meter.

# Piping and Instrumentation Diagrams

## Wiring Diagram

A wiring diagram shows circuit components as simplified shapes with power and signal wiring between the devices, terminal blocks, and input/output (I/O) cards. See Figure 6 for an example. This differs from P&IDs which show pipes and the relative locations of instruments and equipment.

![](images/009ad500938453114420e8d11c35a0786a6c3205005d1b5f07fb5f3216bf3f1a.jpg)  
Figure 6: Example wiring diagram for a pressure transmitter (PIT-3), a 24-volt level transmitter (LIT-6), and a 120-volt level transmitter (LIT-7).

## SCADA Network Diagram

A SCADA (supervisory control and data acquisition) network diagram, also called a SCADA architecture diagram, is a block diagram showing the basic SCADA architecture and communication channels between devices, controllers, and computers. This differs from a P&ID because it lacks the locations of instruments on the piping network and it does not indicate control details. See Figure 7 for an example.

![](images/a51a9c64a2fb53bb9d42b7c68eba62279b8f036e9c6e6c1028bb9cec103a51f6.jpg)  
Figure 7: Example SCADA Network Diagram.  
Source: https://nvlpubs.nist.gov/nistpubs/specialpublications/nist.sp.800-82r2.pdf

### Piping and Instrumentation Diagrams

#### Logic Diagram

Types of logic diagrams included ladder logic diagrams, binary logic diagrams, and Boolean logic diagrams (also called relay logic diagrams). See Figures 8 and 9 for examples. Logic diagrams convey control descriptions pictorially. This differs from a P&ID because it does not show the location of instruments on the piping and does not show communications wiring.

![](images/2d61a349f36a74af2ee5727e56bcc61e5b492bf016e87ed4008bdc90c851568b.jpg)  
Figure 8: Example Ladder Logic Diagram  
Source: https://www.osti.gov/servlets/purl/1468198

![](images/528560fe3bf87e03cb7fd2867c8016602728c3493751e2a151073e68ce7ccff3.jpg)  
Figure 9: Boolean (or relay) logic diagrams showing alternate A or B (left), and alternate A and B (right).  
https://commons.wikimedia.org/wiki/File:Switch\_alternate\_and\_or.png, Copyright © Dysprosia

# Piping and Instrumentation Diagrams

## Industry Standards

There are numerous standards developed for creating P&IDs. The most common standard is ANSI/ISA 5.1 entitled “Instrumentation Symbols and Identification”. A summary of common standards is provided in Table 1.

<table><tr><td rowspan=1 colspan=5>Table 1: Summary of Standards for P&amp;IDs</td></tr><tr><td rowspan=1 colspan=1>Standard No.</td><td rowspan=1 colspan=1>Title</td><td rowspan=1 colspan=1>Pages</td><td rowspan=1 colspan=1>Sector</td><td rowspan=1 colspan=1>Topics Covered</td></tr><tr><td rowspan=1 colspan=1>ANSI/ISA 5.1</td><td rowspan=1 colspan=1>Instrumentation Symbolsand Identification</td><td rowspan=1 colspan=1>128</td><td rowspan=1 colspan=1>All</td><td rowspan=1 colspan=1>Identification Letters TableGraphic SymbolsSymbol Dimensions</td></tr><tr><td rowspan=1 colspan=1>ISA 5.3</td><td rowspan=1 colspan=1>Graphic Symbols forDistributed Control / SharedDisplay Instrumentation,Logic and ComputerSystems</td><td rowspan=1 colspan=1>79</td><td rowspan=1 colspan=1>ComputerSCADA</td><td rowspan=1 colspan=1>SymbolsIdentificationAlarmsComputer Symbolsand Logic</td></tr><tr><td rowspan=1 colspan=1>IEC 60617</td><td rowspan=1 colspan=1>Graphical Symbols forDiagrams</td><td rowspan=1 colspan=1>1900</td><td rowspan=1 colspan=1>All</td><td rowspan=1 colspan=1>Database of Symbols</td></tr><tr><td rowspan=1 colspan=1>ISO 10628</td><td rowspan=1 colspan=1>Diagrams for the Chemicaland Petrochemical Industry</td><td rowspan=1 colspan=1>22</td><td rowspan=1 colspan=1>ChemicalPetro</td><td rowspan=1 colspan=1>Letter Symbols</td></tr><tr><td rowspan=1 colspan=1>ISO 14617Parts 1 to 15</td><td rowspan=1 colspan=1>Graphical Symbols forDiagrams</td><td rowspan=1 colspan=1>300</td><td rowspan=1 colspan=1>All</td><td rowspan=1 colspan=1>Functional LinksControl LoopsProcessing FunctionsLogic Functions</td></tr><tr><td rowspan=1 colspan=1>ISO 15519Parts 1 &amp; 2</td><td rowspan=1 colspan=1>Specification for Diagramsfor Process Industry</td><td rowspan=1 colspan=1>25</td><td rowspan=1 colspan=1>Process</td><td rowspan=1 colspan=1>Block Diagrams, PFDs,P&amp;ID LayoutConnecting LinesInscription, Scale, Limits</td></tr><tr><td rowspan=1 colspan=1>PIP PIC001</td><td rowspan=1 colspan=1>Piping and InstrumentationDiagram DocumentationCriteria</td><td rowspan=1 colspan=1>79</td><td rowspan=1 colspan=1>All</td><td rowspan=1 colspan=1>Industry StandardsEquipment, Piping,Instrumentation, Controls</td></tr><tr><td rowspan=1 colspan=1>EN 62424</td><td rowspan=1 colspan=1>Representation of ProcessControl Engineering</td><td rowspan=1 colspan=1>175</td><td rowspan=1 colspan=1>All</td><td rowspan=1 colspan=1>P&amp;ID Software andControls Interfaces</td></tr></table>

It is common for companies to have their own library of standard symbols and abbreviations. These unique libraries typically include many symbols from reference standards, but also have unique symbols and abbreviations based on the unique systems being designed.

# Piping and Instrumentation Diagrams

## Letter Designations

P&IDs are busy drawings without a lot of space for lengthy descriptions and specifications. Therefore, letter abbreviations (called letter designations) are used for device labels, control loops, and device functions. See Figure 10 for an example of a P&ID with the letter designations defined in a legend.

![](images/f1b3880f41772d2ab9c9685659459aa0ba5ab3c7222cfe6f53e374e3d2f6b937.jpg)  
Figure 10: Example P&ID with a legend defining letter designations. The level sensor 0011 sends a discrete signal to start pump P001 when a high level is reached.  
Source: https://commons.wikimedia.org/wiki/File:Pump\_with\_tank\_pid\_en.svg, modified, Con-struct, CC-BY-SA-3.0

In Figure 10, “M” could mean Motor or Manway. Based on the context, the M1 on the side of the tank is the Manway, and the M in the circle is a Motor for a pump. It is up to the design engineer to make sure any letters used for multiple designations are sufficiently clear on the drawings. Notes can be added to clarify any unclear letter designations.

It is common to utilize a table format for identifying the letter designations for instrument functions (the two or three letters shown inside circles). Table 2 provides the letter designations per ISA 5.1. Many companies develop a standard letter designation table based on common usage. This table can be included with the symbol definitions on a common legend drawing for the P&IDs.

## Piping and Instrumentation Diagrams

<table><tr><td rowspan=1 colspan=6>Table 2: Common Letter Designations in P&amp;IDs for Instrument Functions</td></tr><tr><td rowspan=2 colspan=1>Letter</td><td rowspan=1 colspan=2>First Letter</td><td rowspan=1 colspan=3>Additional Letter(s)</td></tr><tr><td rowspan=1 colspan=1>Measured Value</td><td rowspan=1 colspan=1>Modifier</td><td rowspan=1 colspan=1>Readout orPassive Function</td><td rowspan=1 colspan=1>Output orActive Function</td><td rowspan=1 colspan=1>FunctionModifier</td></tr><tr><td rowspan=1 colspan=1>A</td><td rowspan=1 colspan=1>Analysis</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>Alarm</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>B</td><td rowspan=1 colspan=1>Burner, combustion</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>User choice</td><td rowspan=1 colspan=1>User choice</td><td rowspan=1 colspan=1>User choice</td></tr><tr><td rowspan=1 colspan=1>C</td><td rowspan=1 colspan=1>User&#x27;s choice(usuallyconductivity)</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>Control</td><td rowspan=1 colspan=1>Close</td></tr><tr><td rowspan=1 colspan=1>D</td><td rowspan=1 colspan=1>User&#x27;s choice(usually density)</td><td rowspan=1 colspan=1>Difference,Differential</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>Deviation</td></tr><tr><td rowspan=1 colspan=1>E</td><td rowspan=1 colspan=1>Voltage</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>Sensor</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>F</td><td rowspan=1 colspan=1>Flow rate</td><td rowspan=1 colspan=1>Ratio</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>G</td><td rowspan=1 colspan=1>User&#x27;s choice(usually gauging)</td><td rowspan=1 colspan=1>Gas</td><td rowspan=1 colspan=1>Glass/gauge</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>H</td><td rowspan=1 colspan=1>Hand</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>High</td></tr><tr><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>Current</td><td rowspan=1 colspan=1>Interlock</td><td rowspan=1 colspan=1>Indicate</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>J</td><td rowspan=1 colspan=1>Power</td><td rowspan=1 colspan=1>Scan</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>K</td><td rowspan=1 colspan=1>Time, timeschedule</td><td rowspan=1 colspan=1>Time rate ofchange</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>Control station</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>L</td><td rowspan=1 colspan=1>Level</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>Light</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>Low</td></tr><tr><td rowspan=1 colspan=1>M</td><td rowspan=1 colspan=1>User&#x27;s choice</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>Middle /intermediate</td></tr><tr><td rowspan=1 colspan=1>N</td><td rowspan=1 colspan=1>User&#x27;s choice(usually torque)</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>User choice</td><td rowspan=1 colspan=1>User choice</td><td rowspan=1 colspan=1>User choice</td></tr><tr><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>User&#x27;s choice</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>Orifice</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>Open</td></tr><tr><td rowspan=1 colspan=1>P</td><td rowspan=1 colspan=1>Pressure</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>Point/testconnection</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>Q</td><td rowspan=1 colspan=1>Quantity</td><td rowspan=1 colspan=1>Totalize/integrate</td><td rowspan=1 colspan=1>Totalize/integrate</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>R</td><td rowspan=1 colspan=1>Radiation</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>Record</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>Run</td></tr><tr><td rowspan=1 colspan=1>S</td><td rowspan=1 colspan=1>Speed, frequency</td><td rowspan=1 colspan=1>Safety</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>Switch</td><td rowspan=1 colspan=1>Stop</td></tr><tr><td rowspan=1 colspan=1>T</td><td rowspan=1 colspan=1>Temperature</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>Transmit</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>U</td><td rowspan=1 colspan=1>Multivariable</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>Multifunction</td><td rowspan=1 colspan=1>Multifunction</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1>Vibration,mech. analysis</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>Valve ordamper</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>W</td><td rowspan=1 colspan=1>Weight, force</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>Well or probe</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>User&#x27;s choice (on-off valve as XV)</td><td rowspan=1 colspan=1>X-axis</td><td rowspan=1 colspan=1>Accessory devices</td><td rowspan=1 colspan=1>Unclassified</td><td rowspan=1 colspan=1>Unclassified</td></tr><tr><td rowspan=1 colspan=1>Y</td><td rowspan=1 colspan=1>Event, state,presence, status</td><td rowspan=1 colspan=1>Y-axis</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>Auxiliarydevices</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>Z</td><td rowspan=1 colspan=1>Position, dimension</td><td rowspan=1 colspan=1>Z-axis or SafetyInstrumentedSystem</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>Actuator, driver,or controlelement</td><td rowspan=1 colspan=1></td></tr></table>

For additional clarity, instrument tag abbreviations can be defined as shown in Figure 11. The first letter is from the row (measured variable) and subsequent letters are from the columns (instrument function). For example, LS means “Level Switch” in Figure 11, while LS could mean “Level Switch” or “Level Stop” in Table 2.

<table><tr><td rowspan=1 colspan=2>INSTRUMENT FUNCTIONMEASURED VARIABLE</td><td rowspan=1 colspan=1>ELEMMNT</td><td rowspan=1 colspan=1>TRNTER</td><td rowspan=1 colspan=1>ININIIER</td><td rowspan=1 colspan=1>TRLAYSPEL DCCESCOER</td><td rowspan=1 colspan=1>INDICCTOR</td><td rowspan=1 colspan=1>RECDER</td><td rowspan=1 colspan=1>CONER</td><td rowspan=1 colspan=1>SWIITCH</td><td rowspan=1 colspan=1>LIGHT</td><td rowspan=1 colspan=1>ALARM</td></tr><tr><td rowspan=1 colspan=1>A</td><td rowspan=1 colspan=1>ANALYSIS</td><td rowspan=1 colspan=1>AE</td><td rowspan=1 colspan=1>AT</td><td rowspan=1 colspan=1>AIT</td><td rowspan=1 colspan=1>AY</td><td rowspan=1 colspan=1>Al</td><td rowspan=1 colspan=1>AR</td><td rowspan=1 colspan=1>AC</td><td rowspan=1 colspan=1>AS</td><td rowspan=1 colspan=1>AL</td><td rowspan=1 colspan=1>AA</td></tr><tr><td rowspan=1 colspan=1>B</td><td rowspan=1 colspan=1>BURNER FLAME</td><td rowspan=1 colspan=1>BE</td><td rowspan=1 colspan=1>BT</td><td rowspan=1 colspan=1>BIT</td><td rowspan=1 colspan=1>BY</td><td rowspan=1 colspan=1>BI</td><td rowspan=1 colspan=1>BR</td><td rowspan=1 colspan=1>BC</td><td rowspan=1 colspan=1>BS</td><td rowspan=1 colspan=1>BL</td><td rowspan=1 colspan=1>BA</td></tr><tr><td rowspan=1 colspan=1>C</td><td rowspan=1 colspan=1>CONDUCTIVITY</td><td rowspan=1 colspan=1>CE</td><td rowspan=1 colspan=1>CT</td><td rowspan=1 colspan=1>CIT</td><td rowspan=1 colspan=1>CY</td><td rowspan=1 colspan=1>Cl</td><td rowspan=1 colspan=1>CR</td><td rowspan=1 colspan=1>CC</td><td rowspan=1 colspan=1>CS</td><td rowspan=1 colspan=1>CL</td><td rowspan=1 colspan=1>CA</td></tr><tr><td rowspan=1 colspan=1>D</td><td rowspan=1 colspan=1>DENSITY</td><td rowspan=1 colspan=1>DE</td><td rowspan=1 colspan=1>DT</td><td rowspan=1 colspan=1>DIT</td><td rowspan=1 colspan=1>DY</td><td rowspan=1 colspan=1>DI</td><td rowspan=1 colspan=1>DR</td><td rowspan=1 colspan=1>DC</td><td rowspan=1 colspan=1>DS</td><td rowspan=1 colspan=1>DL</td><td rowspan=1 colspan=1>DA</td></tr><tr><td rowspan=1 colspan=1>E</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>F</td><td rowspan=1 colspan=1>FLOW</td><td rowspan=1 colspan=1>FE</td><td rowspan=1 colspan=1>FT</td><td rowspan=1 colspan=1>FIT</td><td rowspan=1 colspan=1>FY</td><td rowspan=1 colspan=1>Fl</td><td rowspan=1 colspan=1>FR</td><td rowspan=1 colspan=1>FC</td><td rowspan=1 colspan=1>FS</td><td rowspan=1 colspan=1>FL</td><td rowspan=1 colspan=1>FA</td></tr><tr><td rowspan=1 colspan=1>FF</td><td rowspan=1 colspan=1>FLOW RATIO</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>FFY</td><td rowspan=1 colspan=1>FFI</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>FFC</td><td rowspan=1 colspan=1>FFS</td><td rowspan=1 colspan=1>FFL</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>G</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>H</td><td rowspan=1 colspan=1>HAND (MANUAL)</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>HC</td><td rowspan=1 colspan=1>HS</td><td rowspan=1 colspan=1>HL</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>CURRENT</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>IT</td><td rowspan=1 colspan=1>IIT</td><td rowspan=1 colspan=1>IY</td><td rowspan=1 colspan=1>II</td><td rowspan=1 colspan=1>IR</td><td rowspan=1 colspan=1>IC</td><td rowspan=1 colspan=1>IS</td><td rowspan=1 colspan=1>IL</td><td rowspan=1 colspan=1>IA</td></tr><tr><td rowspan=1 colspan=1>J</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>K</td><td rowspan=1 colspan=1>TIME</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>KY</td><td rowspan=1 colspan=1>KI</td><td rowspan=1 colspan=1>KR</td><td rowspan=1 colspan=1>KC</td><td rowspan=1 colspan=1>KS</td><td rowspan=1 colspan=1>KL</td><td rowspan=1 colspan=1>KA</td></tr><tr><td rowspan=1 colspan=1>L</td><td rowspan=1 colspan=1>LEVEL</td><td rowspan=1 colspan=1>LE</td><td rowspan=1 colspan=1>LT</td><td rowspan=1 colspan=1>LIT</td><td rowspan=1 colspan=1>LY</td><td rowspan=1 colspan=1>LI</td><td rowspan=1 colspan=1>LR</td><td rowspan=1 colspan=1>LC</td><td rowspan=1 colspan=1>LS</td><td rowspan=1 colspan=1>LL</td><td rowspan=1 colspan=1>LA</td></tr><tr><td rowspan=1 colspan=1>M</td><td rowspan=1 colspan=1>MOISTURE OR HUMIDITY</td><td rowspan=1 colspan=1>ME</td><td rowspan=1 colspan=1>MT</td><td rowspan=1 colspan=1>MIT</td><td rowspan=1 colspan=1>MY</td><td rowspan=1 colspan=1>MI</td><td rowspan=1 colspan=1>MR</td><td rowspan=1 colspan=1>MC</td><td rowspan=1 colspan=1>MS</td><td rowspan=1 colspan=1>ML</td><td rowspan=1 colspan=1>MA</td></tr><tr><td rowspan=1 colspan=1>N</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>P</td><td rowspan=1 colspan=1>PRESSURE OR VACUUM</td><td rowspan=1 colspan=1>PE</td><td rowspan=1 colspan=1>PT</td><td rowspan=1 colspan=1>PIT</td><td rowspan=1 colspan=1>PY</td><td rowspan=1 colspan=1>PI</td><td rowspan=1 colspan=1>PR</td><td rowspan=1 colspan=1>PC</td><td rowspan=1 colspan=1>PS</td><td rowspan=1 colspan=1>PL</td><td rowspan=1 colspan=1>PA</td></tr><tr><td rowspan=1 colspan=1>PD</td><td rowspan=1 colspan=1>DIFFERENTIAL PRESSURE</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>PDT</td><td rowspan=1 colspan=1>PDIT</td><td rowspan=1 colspan=1>PDY</td><td rowspan=1 colspan=1>PDI</td><td rowspan=1 colspan=1>PDR</td><td rowspan=1 colspan=1>PDC</td><td rowspan=1 colspan=1>PDS</td><td rowspan=1 colspan=1>PDL</td><td rowspan=1 colspan=1>PDA</td></tr><tr><td rowspan=1 colspan=1>Q</td><td rowspan=1 colspan=1>QUANTITY</td><td rowspan=1 colspan=1>QE</td><td rowspan=1 colspan=1>QT</td><td rowspan=1 colspan=1>QIT</td><td rowspan=1 colspan=1>QY</td><td rowspan=1 colspan=1>QI</td><td rowspan=1 colspan=1>QR</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>QS</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>QA</td></tr><tr><td rowspan=1 colspan=1>R</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>S</td><td rowspan=1 colspan=1>SPEED</td><td rowspan=1 colspan=1>SE</td><td rowspan=1 colspan=1>ST</td><td rowspan=1 colspan=1>SIT</td><td rowspan=1 colspan=1>SY</td><td rowspan=1 colspan=1>SI</td><td rowspan=1 colspan=1>SR</td><td rowspan=1 colspan=1>SC</td><td rowspan=1 colspan=1>SS</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>SA</td></tr><tr><td rowspan=1 colspan=1>T</td><td rowspan=1 colspan=1>TEMPERATURE</td><td rowspan=1 colspan=1>TE</td><td rowspan=1 colspan=1>TT</td><td rowspan=1 colspan=1>TIT</td><td rowspan=1 colspan=1>TY</td><td rowspan=1 colspan=1>TI</td><td rowspan=1 colspan=1>TR</td><td rowspan=1 colspan=1>TC</td><td rowspan=1 colspan=1>TS</td><td rowspan=1 colspan=1>TL</td><td rowspan=1 colspan=1>TA</td></tr><tr><td rowspan=1 colspan=1>TD</td><td rowspan=1 colspan=1>DIFFERENTIAL TEMPERATURE</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>TDT</td><td rowspan=1 colspan=1>TDIT</td><td rowspan=1 colspan=1>TDY</td><td rowspan=1 colspan=1>TDI</td><td rowspan=1 colspan=1>TDR</td><td rowspan=1 colspan=1>TDC</td><td rowspan=1 colspan=1>TDS</td><td rowspan=1 colspan=1>TDL</td><td rowspan=1 colspan=1>TDA</td></tr><tr><td rowspan=1 colspan=1>U</td><td rowspan=1 colspan=1>MULTIVARIABLE</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>UI</td><td rowspan=1 colspan=1>UR</td><td rowspan=1 colspan=1>UC</td><td rowspan=1 colspan=1>US</td><td rowspan=1 colspan=1>UL</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1>VISCOSITY</td><td rowspan=1 colspan=1>VE</td><td rowspan=1 colspan=1>VT</td><td rowspan=1 colspan=1>VIT</td><td rowspan=1 colspan=1>VY</td><td rowspan=1 colspan=1>VI</td><td rowspan=1 colspan=1>VR</td><td rowspan=1 colspan=1>VC</td><td rowspan=1 colspan=1>VS</td><td rowspan=1 colspan=1>VL</td><td rowspan=1 colspan=1>VA</td></tr><tr><td rowspan=1 colspan=1>w</td><td rowspan=1 colspan=1>WEIGHT</td><td rowspan=1 colspan=1>WE</td><td rowspan=1 colspan=1>WT</td><td rowspan=1 colspan=1>WIT</td><td rowspan=1 colspan=1>WY</td><td rowspan=1 colspan=1>WI</td><td rowspan=1 colspan=1>WR</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>WS</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>WA</td></tr><tr><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>UNCLASSIFIED</td><td rowspan=1 colspan=1>XE</td><td rowspan=1 colspan=1>XT</td><td rowspan=1 colspan=1>XIT</td><td rowspan=1 colspan=1>XY</td><td rowspan=1 colspan=1>xI</td><td rowspan=1 colspan=1>XR</td><td rowspan=1 colspan=1>XC</td><td rowspan=1 colspan=1>XS</td><td rowspan=1 colspan=1>XL</td><td rowspan=1 colspan=1>XA</td></tr><tr><td rowspan=1 colspan=1>XV</td><td rowspan=1 colspan=1>VIBRATION</td><td rowspan=1 colspan=1>XVE</td><td rowspan=1 colspan=1>XVT</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>XVY</td><td rowspan=1 colspan=1>XVI</td><td rowspan=1 colspan=1>XVR</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>xvs</td><td rowspan=1 colspan=1>XVL</td><td rowspan=1 colspan=1>XVA</td></tr><tr><td rowspan=1 colspan=1>Y</td><td rowspan=1 colspan=1>STATUS</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>YI</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>YL</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>Z</td><td rowspan=1 colspan=1>POSITION</td><td rowspan=1 colspan=1>ZE</td><td rowspan=1 colspan=1>ZT</td><td rowspan=1 colspan=1>ZIT</td><td rowspan=1 colspan=1>ZY</td><td rowspan=1 colspan=1>Zl</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>zS</td><td rowspan=1 colspan=1>ZL</td><td rowspan=1 colspan=1></td></tr></table>

Figure 11: Example Instrument Tag Abbreviations Table from a P&ID legend drawing.

Instrument control abbreviations are shown to the upper right of instrument tags. These can also be defined in a P&ID legend, as shown in Figure 12.

![](images/4335b56ec20d468eccf92bd0d67f5296d35cdd94b051252dd80745529197748b.jpg)

<table><tr><td>AHC</td><td>AUTO/HOLD/CLOSE</td><td>OSC</td><td>OPEN/STOP/CLOSED</td></tr><tr><td>A/M</td><td>AUTO/MANUAL</td><td></td><td></td></tr><tr><td>DEV</td><td>DEVIATION</td><td>P/P</td><td>PUSH/PULL</td></tr><tr><td>HOA</td><td>HAND/OFF/AUTO</td><td>RL</td><td>RAISE/LOWER</td></tr><tr><td>HOR</td><td>HAND/OFF/REMOTE</td><td>RSL</td><td>RAISE/STOP/LOWER</td></tr><tr><td>L/R</td><td>LOCAL/REMOTE</td><td>S/D</td><td>SHUTDOWN</td></tr><tr><td>L/O/R</td><td>LOCAL/OFF/REMOTE</td><td>SEL</td><td>SELECT</td></tr><tr><td>MOA</td><td>MANUAL/OFF/AUTO</td><td>S/LOS</td><td>START/LOCKOUT STOP</td></tr><tr><td>0/0</td><td>ON/OFF</td><td>SP</td><td>SET POINT</td></tr><tr><td>OCA</td><td>OPEN/CLOSE/AUTO</td><td>SR</td><td>START/RESET</td></tr><tr><td>O/C</td><td>OPEN/CLOSE</td><td>S/S</td><td>STOP/START</td></tr></table>

Figure 12: Example abbreviations for instrument control functions. These letter designations are commonly placed to the upper right of instrument tag circles, where the (XXX) is shown.

The simplest control device is the O/O (On/Off) switch, as shown in Figure 13.

![](images/aef8300026d070f9e5803f51c2bc6cf4879078cb7a4a75a612b4a6d7b1d0044c.jpg)  
Figure 13: O/O hand switch (HS) on a control panel, with On and Off functions. Source: https://commons.wikimedia.org/wiki/File:On-Off\_Switch.jpg, Jszack, CC-BY-SA-2.5

# Piping and Instrumentation Diagrams

HOA stands for Hand/Off/Auto, which is common for a switch that controls equipment with a motor. See Figure 14 for an example of an HOA selector switch. This is similar to HOR (Hand/Off/Remote) in which the device can be controlled remotely (either automatically or by a remote user through a control panel or HMI (Human-Machine Interface) software.

![](images/a5fb28248b5b4e68a16fb4afeadb7d3e0d97da00a36303397efd4b5c0b136feb.jpg)  
Figure 14: Selector/hand switch with HOA functions:

1) HAND means the device will be on with no automated controls,

2) OFF means the device will be off with no automated controls, and 3) AUTO means the device will be turned on and off through automated controls.

# Piping and Instrumentation Diagrams

## Example Problem 1

Engineer Phelix is reading a P&ID drawing to understand the functions available at the local control panel (LCP) for ball valve VLV-311, as shown below. Help Phelix by writing out the letter designations based on Figures 11 and 12.

![](images/b1bd761e7720a64bf3ff4fa360a69333d39214c689b5c11318cb503fa86fe9fd.jpg)

Solution:

Letter designations have been spelled out in red in the below diagram.

![](images/0af0959a7fe4d53974a77abd7f2920e0ca27bd44fd9e75185284f57b6eb4dc37.jpg)

Note that the \(" [ "\) could mean Current or Interlock. Based on the context of being in a local control panel with switches, the term interlock is a better fit. An interlock is an electrical device for connecting the function of different components. For example, when the hand switch is set to \(" 0 p e { n } "\) , electrical power is sent to the valve motor via an interlock.

# Piping and Instrumentation Diagrams

## Symbols

P&IDs are full of symbols. See Figures 15 to 17 for example P&IDs with various symbols.

Common items that have symbols on a P&ID include:

• Instruments (flow, level, pressure, temperature, weight, pH, chlorine, etc.)

• Control functions (field, panel front, panel rear, SCADA, etc.)

• Interfaces to and from external processes (large arrows are common)

• Valves

• Actuators

• Motors

• Pumps

• Fans, Blowers, and Compressors

• Miscellaneous devices (tanks, mixers, strainer, gate, injection, seal water, etc.)

• Communications wiring (discrete, analog, ethernet, fiber optic, etc.)

These symbols should be defined on a legend drawing.

Figures 18a and 18b show common P&ID symbols for piping, valves, and equipment, per ISO 10628 and ISO 14617.