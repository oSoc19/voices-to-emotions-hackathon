import React from 'react';
import styled from '@emotion/styled';

import Dropzone from '../components/dropzone';

export type DropzonePageProps = {
  onFileUpload: (file: FileList) => any;
};

const Wrapper = styled.div(() => {
  return {
    display: 'grid',
    textAlign: 'center'
  };
});

export default function DropzonePage(props: DropzonePageProps) {
  let { onFileUpload } = props;

  const handleSelectFile = (selectedFiles: FileList) => {
    if (!selectedFiles.length) return;

    onFileUpload(selectedFiles);
  };

  const handleDropzoneTrigger = () => {
    let inputElement = document.createElement('input');
    inputElement.type = 'file';
    inputElement.multiple = false;

    inputElement.addEventListener('change', function() {
      if (!this.files) return;
      // @ts-ignore...
      handleSelectFile([...this.files]);
    });
    inputElement.dispatchEvent(new MouseEvent('click'));
  };

  return (
    <Wrapper>
      <h1>Voices To Emotions</h1>
      <h2>Upload an audio file to get started...</h2>
      <Dropzone onTrigger={handleDropzoneTrigger} onDrop={handleSelectFile}></Dropzone>
    </Wrapper>
  );
}
