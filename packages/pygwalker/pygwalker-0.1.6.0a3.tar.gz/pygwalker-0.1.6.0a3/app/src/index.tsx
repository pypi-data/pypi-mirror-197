import React from 'react';
import ReactDOM from 'react-dom';
import { GraphicWalker } from '@kanaries/graphic-walker'
import type { IGWProps } from '@kanaries/graphic-walker/dist/App'
import type { IGlobalStore } from '@kanaries/graphic-walker/dist/store'
// import type { IGWProps } from 'gwalker/App'

import Options from './components/options';

const App: React.FC<IGWProps> = (props) => {
  const ref = React.useRef<IGlobalStore | null>(null);
  return (<React.StrictMode>
    <Options {...props} storeRef={ref} />
    <GraphicWalker {...props} storeRef={ref} />
  </React.StrictMode>);
}

function GWalker(props: any, id: string) {
    // GWalkerMap[id] = c;
    ReactDOM.render(<App {...props}></App>, document.getElementById(id)
  );
}

// export {IGWProps}
export default { GWalker }