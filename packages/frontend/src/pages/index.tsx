import React from 'react';
import styled from '@emotion/styled';

import SEO from '../components/seo';
import DropzonePage from '../components/dropzone-page';
import ResultPage from '../components/result-page';

export type FileUploadItem = {
  file: File;
  state: 'loading' | 'error' | 'success' | 'none';
};

const Main = styled.main(() => {
  return {
    maxWidth: 960,
    padding: 20,
    margin: '0 auto'
  };
});

export default function IndexPage() {
  let [file, setFile] = React.useState<FileList | null>(null);

  return (
    <>
      <SEO title="Home" />
      <Main>{file ? <ResultPage file={file} /> : <DropzonePage onFileUpload={setFile} />}</Main>
    </>
  );
}
