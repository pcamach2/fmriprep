import json
import fmriprep.utils.misc as misc
import re
import unittest

class TestCollectBids(unittest.TestCase):
    @classmethod
    def setUp(self):
        self.dataset = "test_data/aa_conn"
        try:
            self.imaging_data = misc.collect_bids_data(self.dataset)
        except Exception as e:
            url = "http://googledrive.com/host/0BxI12kyv2olZbl9GN3BIOVVoelE"
            raise Exception("Couldn't find data at " + self.dataset + 
                            ". Download from " + url) from e

    def assert_key_exists(self, template, key):
        for subject in self.imaging_data:
            for session in self.imaging_data[subject]:
                self.assertIn(template.format(subject=subject),
                              self.imaging_data[subject][session][key])

    def test_collect_bids_data(self):
        ''' test data has at least one subject with at least one session '''
        self.assertNotEqual(0, len(self.imaging_data))
        self.assertNotEqual(0, len(next(iter(self.imaging_data.values()))))

    def test_epi(self):
        epi_template = "{subject}/func/{subject}_task-rest_acq-LR_run-1_bold.nii.gz"
        self.assert_key_exists(epi_template, 'epi')

    def test_epi_meta(self):
        epi_meta_template = "{subject}/func/{subject}_task-rest_acq-LR_run-1_bold.json"
        self.assert_key_exists(epi_meta_template, 'epi_meta')

    def test_sbref(self):
        sbref_template = "{subject}/func/{subject}_task-rest_acq-LR_run-1_sbref.nii.gz"
        self.assert_key_exists(sbref_template, 'sbref')

    def test_sbref_meta(self):
        sbref_meta_template = "{subject}/func/{subject}_task-rest_acq-LR_run-1_sbref.json"
        self.assert_key_exists(sbref_meta_template, 'sbref_meta')
    
    def test_t1(self):
        t1_template = "{subject}/anat/{subject}_run-1_T1w.nii.gz"
        self.assert_key_exists(t1_template, 't1')

    def test_fieldmaps(self):
        for subject in self.imaging_data:
            fieldmap_pattern = r"{0}\/fmap\/{0}_dir-[0-9]+_run-[0-9]+_epi\.nii\.gz".format(subject)
            for session in self.imaging_data[subject]:
                for fieldmap in self.imaging_data[subject][session]['fieldmaps']:
                    match = re.search(fieldmap_pattern, fieldmap)
                    self.assertTrue(match)
    
    def test_fieldmaps_meta(self):
        for subject in self.imaging_data:
            fieldmap_meta_pattern = r"{0}\/fmap\/{0}_dir-[0-9]+_run-[0-9]+_epi\.json".format(subject)
            for session in self.imaging_data[subject]:
                for fieldmap_meta in self.imaging_data[subject][session]['fieldmaps_meta']:
                    match = re.search(fieldmap_meta_pattern, fieldmap_meta)
                    self.assertTrue(match)
    
        
if __name__ == '__main__':
    unittest.main() 
    #dataset = "../../test_data/aa_conn"
    #imaging_data = misc.collect_bids_data(dataset)