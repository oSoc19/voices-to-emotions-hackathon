import React from 'react';
import styled from '@emotion/styled';
import { H1, H2 } from '@blazingly-design/heading';
import Paragraph from '@blazingly-design/paragraph';

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
    textAlign: 'center',
    gridGap: 40
  };
});

const TextBalloon = styled.div<{ hasContent: boolean }>(({ hasContent }) => {
  return {
    marginTop: 50,
    display: 'inline-block',
    padding: 15,
    textAlign: 'left',
    backgroundColor: '#D81E5B',
    borderRadius: '10px 10px 10px 0',
    transition: 'max-width 5s, max-height 5s',
    maxHeight: hasContent ? '100%' : 0,
    maxWidth: hasContent ? '100%' : 0,
    textOverflow: 'ellipsis',
    whiteSpace: 'nowrap',
    overflow: 'hidden'
  };
});

export default function DropzonePage(props: DropzonePageProps) {
  let { file } = props;
  let [res, setRes] = React.useState<null | ResultType>(null);

  if (!file) throw new Error('no file...');

  React.useEffect(() => {
    setTimeout(() => {
      setRes({
        text: 'This should be a transcript of the audio file...',
        emotion: 0.3
      });
    }, 2500);
  }, [true]);

  return (
    <>
      <Wrapper>
        <Loader finished={!!res} positive={res ? res.emotion < 0.5 : undefined}>
          {res ? Math.round(res.emotion * 100) : ''}
        </Loader>
      </Wrapper>
      <TextBalloon hasContent={!!res}>
        <Paragraph color="white">{res ? res.text : ''}</Paragraph>
      </TextBalloon>
    </>
  );
}
