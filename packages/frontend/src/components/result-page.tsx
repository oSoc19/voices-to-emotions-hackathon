import React from 'react';
import styled from '@emotion/styled';

import Loader from '../components/loader';

export type ResultType = {
  text: string;
  emotion: number;
};

export type DropzonePageProps = {
  file: FileList;
};

const Wrapper = styled.div(() => {
  return {
    display: 'grid',
    textAlign: 'center'
  };
});

export default function DropzonePage(props: DropzonePageProps) {
  let { file } = props;
  let [res, setRes] = React.useState<null | ResultType>(null);

  if (!file) throw new Error('no file...');

  React.useEffect(() => {
    setTimeout(() => {
      setRes({
        text: 'Thank you for calling.',
        emotion: 0.3
      });
    }, 2500);
  }, [true]);

  return (
    <Wrapper>
      {res ? <h1>Result</h1> : <h1>Loading</h1>}
      <Loader finished={!!res} positive={res ? res.emotion < 0.5 : undefined} />
      {res && (
        <div>
          <h2>Analysed Text</h2>
          <p>{res.text}</p>
        </div>
      )}
    </Wrapper>
  );
}
