import React from 'react';
import { JupyterFrontEnd } from '@jupyterlab/application';
import { ICommandPalette, ReactWidget } from '@jupyterlab/apputils';
import { notificationList } from './notifications';
import { ILauncher } from '@jupyterlab/launcher';
import { LabIcon } from '@jupyterlab/ui-components';

class ExampleWidget extends ReactWidget {
  constructor() {
    super();
    this.addClass('welcome-widget');
    this.addClass('jp-RenderedHTMLCommon');
    this.id = 'welcome-widget';
    this.title.label = 'Welcome';
    this.title.closable = true;
    this.title.iconClass = 'fa fa-door-open';
  }

  render() {
    return (
      <div className="welcome-widget-content">
        <div className="inner">
          <h1>Let's Run Some Agent Based Models!</h1>
          <p>
            <i>
              Tip: To reopen this page, open the command palette (
              <kbd>Shift</kbd> + <kbd>CMD/CTRL</kbd> + <kbd>C</kbd>) and search
              "Welcome Page".
            </i>
          </p>
          <h2>About the Epistemix Platform</h2>
          <p>
            The Epistemix Platform is a web-based integrated development
            environment that will enable you to design, run, and analyze
            agent-based models (ABMs) with FRED - the Framework for
            Reconstructing Epidemiological Dynamics.
          </p>
          <p>
            The Epistemix Platform provides access to our new FRED modeling
            language version, a custom ABM data management system, and a
            detailed synthetic population of the USA, all designed for flexible
            and efficient modeling of large-scale, real-world, social dynamics.
          </p>
          <p>
            The Epistemix Platform embeds our most recent FRED ABMs within a
            Python-based Jupyter notebook, a convenient environment for model
            development. Users who are fluent in Python and/or Jupyter should
            find it easy to navigate, but even users who are not data scientists
            can run and understand all of the models presented here by following
            the instructions provided below.
          </p>
          <h2>Introductory Models</h2>
          <p>
            A variety of introductory ABMs are provided here. You can easily run
            each ABM, and then examine the FRED code behind the simulation. We
            will discuss how to do so in greater detail later. If you would like
            to jump right in, the following introductory ABMs are available:
          </p>
          <ul>
            <li>
              <p>
                "The Epstein Rebellion Model" - Civil violence in Grand Isle
                County, Vermont
              </p>
            </li>
            <li>
              <p>
                "Influenza – Mitigations" - Staying home by income in Kewaunee
                County, Wisconsin
              </p>
            </li>
            <li>
              <p>
                "The Schelling Housing Model" - Racial segregation in Kewaunee
                County, Wisconsin
              </p>
            </li>
            <li>
              <p>
                "Synthesizing Agent Variables" - Music listening behaviors in
                Butte County Idaho
              </p>
            </li>
            <li>
              <p>
                "User Product Journey" - App purchasers in Kewaunee County,
                Wisconsin
              </p>
            </li>
          </ul>
          <p>
            <i>
              Note: To keep these introductory model runtimes as low as
              possible, all of the ABM simulations presented here have
              intentionally been set in small US counties, but you should know
              that, with sufficient memory, every FRED model can be run on any
              county in the USA using exactly the same FRED code on the specific
              synthetic population for that county.
            </i>
          </p>
          <h1>Getting Started</h1>
          <h2>Running an Epistemix ABM in a Jupyter Notebook</h2>
          <p>
            To open an Introductory Model, click on the folder menu to the left
            to navigate to the model that you want. Once in a the subdirectory
            of the desired model, click on the file with the orange, Jupyter
            notebook icon (
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="16"
              viewBox="0 0 22 22"
              data-icon="ui-components:notebook"
              data-icon-id="c278ba79-ed58-4b3c-b205-da6692320ffc"
            >
              <g
                className="jp-notebook-icon-color jp-icon-selectable"
                fill="#EF6C00"
              >
                <path d="M18.7 3.3v15.4H3.3V3.3h15.4m1.5-1.5H1.8v18.3h18.3l.1-18.3z"></path>
                <path d="M16.5 16.5l-5.4-4.3-5.6 4.3v-11h11z"></path>
              </g>
            </svg>
            ) to open the simulation's notebook. The Jupyter notebook simulation
            page displays explanatory text, cells that contain code written in
            Python, and cells that display model output results.
          </p>
          <p>
            Next, to run the model, on the notebook's menu bar, click to expand
            the “Run” tab, and then click “Run All Cells.” For more information
            about Jupyter Notebooks see{' '}
            <a href="https://jupyter.org/try-jupyter/retro/notebooks/?path=notebooks/Intro.ipynb">
              here
            </a>
            .
          </p>
          <h2>Modifying a Jupyter Notebook</h2>
          <p>
            The Jupyter notebook page for any given model displays a series of
            cells that contain Python code for executing the FRED program. Users
            who are fluent in Python can modify the inputs, execution, and
            outputs of the FRED model as they wish. Those not fluent in Python
            can ignore this code for now, and just run the models.
          </p>
          <h2>Viewing the FRED Code for a Model</h2>
          <p>
            The FRED code is not displayed directly on the Python-based Jupyter
            notebook page. To see the FRED code behind the model, click on the
            folder for the model you want, then click on the code files marked
            by the Epistemix logo (
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="16"
              viewBox="0 0 320 320"
              data-icon="fredIcon"
              data-icon-id="6b3bcb34-5d99-4864-ba66-6cd2a7aaf3a8"
            >
              <g className="jp-icon-selectable">
                <path
                  d="M225.3 143.6v32.8h-91.8v32.8H245V242H81v-98.4h144.3ZM81 110.8V78h157.4v32.8H81Z"
                  fill="#FFF"
                ></path>
              </g>
            </svg>
            ) and which end in “.fred." Most FRED ABMs consist of several
            modular FRED code files, most of which are hierarchically linked to
            others.
          </p>
          <h2>Editing the FRED Code for a Model</h2>
          <p>
            The FRED Modeling Language Guide can be accessed{' '}
            <a href="https://docs.epistemix.com/projects/lang-guide/">here</a>.
            If you area already familiar with FRED and wish to modify these
            models, you can do so by opening the FRED code file, modifying it,
            then saving it by pressing <kbd>CMD/CTRL</kbd> + <kbd>S</kbd>.
          </p>
          <p>
            Next, go back to the main menu on the left, reopen the Jupyter
            notebook page for the model, and run the model again. To restore all
            the FRED code on the Epistemix Platform to its unmodified state, you
            can go to the top folder in the menu on the left and run the
            Reset-Guides function. Note that new visitors should probably not
            try to modify the FRED code.
          </p>
          <h2>Tracking the Progress of an ABM Run</h2>
          <p>
            Once a FRED model run has started, you can track its progress by
            watching the small circle in the upper right corner of the
            notebook's menu bar (next to “Python 3 ipykernel”). Note that this
            circle will not be visible when editing other file types.
          </p>
          <p>
            The circle will be empty before the run, change to white when the
            model is accessed, and once the run is started it will show a
            clocklike wedge that expands as the model moves toward completion.
            By hovering your cursor over the circle, a text box will appear
            showing the number of Jupyter notebook cells executed and the
            elapsed runtime.
          </p>
          <h1>Learn FRED with the Epistemix Quickstart Guide</h1>
          <p>
            The Epistemix Quickstart Guide is a series of ten step-by-step
            lessons on how to use FRED, each of which is illustrated with an
            interesting, new, short tutorial FRED model. The user can navigate
            these lessons by following instructions above for Running, Viewing,
            Modifying, and Tracking FRED. To begin the lessons, go the menu on
            the left, click on the most recent version of the Quickstart Guide,
            and begin with lesson 001.
          </p>
          <p>The lessons are as follows:</p>
          <ul>
            <li>
              <p>001 - Minimal FRED</p>
            </li>
            <li>
              <p>002 - Conditions and States</p>
            </li>
            <li>
              <p>003 - Agents</p>
            </li>
            <li>
              <p>004 - Multiple Conditions</p>
            </li>
            <li>
              <p>005 - Places</p>
            </li>
            <li>
              <p>006 - Interactions</p>
            </li>
            <li>
              <p>007 - Transmission</p>
            </li>
            <li>
              <p>008 - Agents and Places</p>
            </li>
            <li>
              <p>009 - Control Structures</p>
            </li>
            <li>
              <p>010 - Data Input and Output</p>
            </li>
            <li>
              <p>011 - Running FRED Through the Client Object</p>
            </li>
          </ul>
          <h1>Creating Your Own FRED Models</h1>
          <p>
            This Epistemix Platform can be used to create entirely new FRED
            models. To do this, go to the main menu folder on the left, right
            click to add a new folder. In that newly created folder, right click
            again to add a new Jupyter Notebook page, and name the folder and
            Notebook.
          </p>
          <p>
            Add the necessary Python code to the cells in the Jupyter Notebook,
            and write the FRED code as one or more text files, which you should
            then save as FRED files by replacing the file extension (.txt) with
            .fred before you save it.
          </p>
          <p>
            You may find it convenient to borrow blocks of Python code or FRED
            code from the numerous Introductory, Quickstart, and Demonstration
            models that are already available on the Platform.
          </p>
          <h2>Synthetic Population</h2>
          <p>
            Below you will find a list of synthetic populations that are freely
            available synthetic on the platform.
          </p>
          <table>
            <tbody>
              <tr>
                <th>
                  <b>County</b>
                </th>
                <th>
                  <b>State</b>
                </th>
                <th>
                  <b>FIPS Code</b>
                </th>
                <th>
                  <b>2010 Population</b>
                </th>
              </tr>
              <tr>
                <td>Park</td>
                <td>Colorado</td>
                <td>08093</td>
                <td>15960</td>
              </tr>
              <tr>
                <td>Clarke</td>
                <td>Georgia</td>
                <td>13059</td>
                <td>107247</td>
              </tr>
              <tr>
                <td>Butte</td>
                <td>Idaho</td>
                <td>16023</td>
                <td>2838</td>
              </tr>
              <tr>
                <td>New York</td>
                <td>New York</td>
                <td>36061</td>
                <td>1515118</td>
              </tr>
              <tr>
                <td>Lenoir</td>
                <td>North Carolina</td>
                <td>37107</td>
                <td>57824</td>
              </tr>
              <tr>
                <td>Erie</td>
                <td>Pennsylvania</td>
                <td>42049</td>
                <td>266460</td>
              </tr>
              <tr>
                <td>Jefferson</td>
                <td>Pennsylvania</td>
                <td>42065</td>
                <td>44594</td>
              </tr>
              <tr>
                <td>Loving</td>
                <td>Texas</td>
                <td>48301</td>
                <td>70</td>
              </tr>
              <tr>
                <td>Grand Isle</td>
                <td>Vermont</td>
                <td>50013</td>
                <td>6965</td>
              </tr>
              <tr>
                <td>Dane</td>
                <td>Wisconsin</td>
                <td>55025</td>
                <td>473566</td>
              </tr>
              <tr>
                <td>Kewaunee</td>
                <td>Wisconsin</td>
                <td>55061</td>
                <td>20259</td>
              </tr>
            </tbody>
          </table>
          <h1>Epistemix Resources</h1>
          <h2>Documentation</h2>
          <p>
            Users can access the Epistemix Documentation at{' '}
            <a href="https://docs.epistemix.com/">docs.epistemix.com</a>. This
            site provides useful information about how to build models using
            FRED.
          </p>
          <ul>
            <li>
              <a href="https://docs.epistemix.com/">Documentation Home Page</a>
            </li>
            <li>
              <a href="https://docs.epistemix.com/projects/lang-guide/">
                FRED Modeling Language Guide
              </a>
            </li>
            <li>
              <a href="https://docs.epistemix.com/projects/lang-ref/">
                FRED Language Alphabetical Lookup
              </a>
            </li>
          </ul>
          <h2>Additional Resources</h2>
          <ul>
            <li>
              <a href="https://epistemix.discourse.group/">Discourse Forum</a>
            </li>
            <li>
              <a href="https://blog.epistemix.com/blog/">Epistemix Blog</a>
            </li>
          </ul>
          <p>
            For any other questions, please email{' '}
            <a href="mailto:learning@epistemix.com">learning@epistemix.com</a>.
          </p>
          <h1>Parting Notes</h1>
          <p>
            Changes made by the user to the contents of the ABMs in the
            pre-populated folders on this site are not considered permanent.
            Updates made by Epistemix to the folders containing these guides can
            cause any changes that you may have made to them to be overwritten.
            When editing, duplicating, or writing a model, ensure that you are
            not working in a subdirectory of one of the pre-populated folders.
          </p>
          <p>
            Caution should be exercised when running models that have an
            extremely large population. If insufficient memory is available to
            run the model, the process may be killed.
          </p>
          <h2>Latest Updates</h2>
          <ul className="welcome-notifications">
            {notificationList.map(n => {
              return (
                <li key={n.date}>
                  <i className="notification-date">{n.date}</i>
                  <div dangerouslySetInnerHTML={{ __html: n.description }} />
                </li>
              );
            })}
          </ul>
        </div>
      </div>
    );
  }
}

export function registerWelcomePage(
  app: JupyterFrontEnd,
  palette: ICommandPalette,
  launcher: ILauncher
): void {
  const command = 'welcome-page:open';

  const createCommand = () => {
    const widget = new ExampleWidget();
    app.shell.add(widget, 'main');
  };

  app.restored.then(() => {
    const widgets = app.shell.widgets('main');
    if (!widgets.next()) {
      createCommand();
    }
  });

  app.commands.addCommand(command, {
    label: 'Welcome Page',
    execute: () => {
      createCommand();
    },
    iconClass: 'jp-icon-contrast0',
    icon: new LabIcon({
      name: 'Welcome',
      svgstr:
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 576 512"><path d="M320 32c0-9.9-4.5-19.2-12.3-25.2S289.8-1.4 280.2 1l-179.9 45C79 51.3 64 70.5 64 92.5V448H32c-17.7 0-32 14.3-32 32s14.3 32 32 32H96 288h32V480 32zM256 256c0 17.7-10.7 32-24 32s-24-14.3-24-32s10.7-32 24-32s24 14.3 24 32zm96-128h96V480c0 17.7 14.3 32 32 32h64c17.7 0 32-14.3 32-32s-14.3-32-32-32H512V128c0-35.3-28.7-64-64-64H352v64z" fill="#d2d8f7" /></svg>'
    })
  });

  launcher.add({ command, category: 'Other' });

  palette.addItem({ command, category: 'my-category' });
}
