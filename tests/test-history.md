\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status'

======================================================================
ERROR: test_batch_metric_extraction (tests.test_agents.TestMetricExtractor.test_batch_metric_extraction)
Test batch extraction of metrics for multiple sessions.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_agents.py", line 128, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status', 'duration_ms'

======================================================================
ERROR: test_extract_balloon_risk_metrics (tests.test_agents.TestMetricExtractor.test_extract_balloon_risk_metrics)
Test extraction of balloon risk metrics.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_agents.py", line 128, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status', 'duration_ms'

======================================================================
ERROR: test_extract_metrics_insufficient_data (tests.test_agents.TestMetricExtractor.test_extract_metrics_insufficient_data)        
Test metric extraction with insufficient data.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_agents.py", line 128, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status', 'duration_ms'

======================================================================
ERROR: test_generate_comparative_report (tests.test_agents.TestReportGenerator.test_generate_comparative_report)
Test generation of comparative report.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_agents.py", line 395, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status', 'duration_ms'

======================================================================
ERROR: test_generate_report_no_traits (tests.test_agents.TestReportGenerator.test_generate_report_no_traits)
Test report generation for session without trait profiles.        
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_agents.py", line 395, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status', 'duration_ms'

======================================================================
ERROR: test_generate_session_report (tests.test_agents.TestReportGenerator.test_generate_session_report)
Test generation of session report.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_agents.py", line 395, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status', 'duration_ms'

======================================================================
ERROR: test_infer_session_traits (tests.test_agents.TestTraitInferencer.test_infer_session_traits)
Test trait inference for a session.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_agents.py", line 277, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status'

======================================================================
ERROR: test_infer_traits_insufficient_metrics (tests.test_agents.TestTraitInferencer.test_infer_traits_insufficient_metrics)        
Test trait inference with insufficient metrics.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_agents.py", line 277, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status'

======================================================================
ERROR: test_validate_trait_profile (tests.test_agents.TestTraitInferencer.test_validate_trait_profile)
Test trait profile validation.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_agents.py", line 277, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status'

======================================================================
ERROR: test_bulk_session_listing_performance (tests.test_api.TestAPIPerformance.test_bulk_session_listing_performance)
Test performance of listing many sessions.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_api.py", line 519, in setUp
    self._create_bulk_test_data()
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_api.py", line 525, in _create_bulk_test_data
    session = BehavioralSession(
              ^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status'

======================================================================
ERROR: test_pagination_functionality (tests.test_api.TestAPIPerformance.test_pagination_functionality)
Test API pagination functionality.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_api.py", line 519, in setUp
    self._create_bulk_test_data()
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_api.py", line 525, in _create_bulk_test_data
    session = BehavioralSession(
              ^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status'

======================================================================
ERROR: test_create_behavioral_event (tests.test_api.TestBehavioralDataAPI.test_create_behavioral_event)
Test creating behavioral events via API.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_api.py", line 41, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status'

======================================================================
ERROR: test_create_behavioral_session (tests.test_api.TestBehavioralDataAPI.test_create_behavioral_session)
Test creating a new behavioral session via API.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_api.py", line 41, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status'

======================================================================
ERROR: test_create_invalid_behavioral_event (tests.test_api.TestBehavioralDataAPI.test_create_invalid_behavioral_event)
Test creating invalid behavioral event via API.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_api.py", line 41, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status'

======================================================================
ERROR: test_list_behavioral_events (tests.test_api.TestBehavioralDataAPI.test_list_behavioral_events)
Test listing behavioral events via API.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_api.py", line 41, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status'

======================================================================
ERROR: test_list_behavioral_sessions (tests.test_api.TestBehavioralDataAPI.test_list_behavioral_sessions)
Test listing behavioral sessions via API.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_api.py", line 41, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status'

======================================================================
ERROR: test_retrieve_behavioral_session (tests.test_api.TestBehavioralDataAPI.test_retrieve_behavioral_session)
Test retrieving a specific behavioral session via API.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_api.py", line 41, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status'

======================================================================
ERROR: test_extract_metrics_api (tests.test_api.TestMetricExtractionAPI.test_extract_metrics_api)
Test metric extraction via API.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_api.py", line 160, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status'

======================================================================
ERROR: test_extract_metrics_invalid_session (tests.test_api.TestMetricExtractionAPI.test_extract_metrics_invalid_session)
Test metric extraction with invalid session ID.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_api.py", line 160, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status'

======================================================================
ERROR: test_list_behavioral_metrics (tests.test_api.TestMetricExtractionAPI.test_list_behavioral_metrics)
Test listing behavioral metrics via API.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_api.py", line 160, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status'

======================================================================
ERROR: test_generate_report_api (tests.test_api.TestReportGenerationAPI.test_generate_report_api)
Test report generation via API.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_api.py", line 356, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status', 'duration_ms'

======================================================================
ERROR: test_generate_report_invalid_session (tests.test_api.TestReportGenerationAPI.test_generate_report_invalid_session)
Test report generation with invalid session ID.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_api.py", line 356, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status', 'duration_ms'

======================================================================
ERROR: test_create_trait_profile (tests.test_api.TestTraitInferenceAPI.test_create_trait_profile)
Test creating trait profile via API.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_api.py", line 251, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status'

======================================================================
ERROR: test_infer_traits_api (tests.test_api.TestTraitInferenceAPI.test_infer_traits_api)
Test trait inference via API.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_api.py", line 251, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status'

======================================================================
ERROR: test_list_trait_profiles (tests.test_api.TestTraitInferenceAPI.test_list_trait_profiles)
Test listing trait profiles via API.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_api.py", line 251, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status'

======================================================================
ERROR: test_predict_all_traits (tests.test_trait_mapping.TestScientificTraitModel.test_predict_all_traits)
Test prediction of all traits using scientific models.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_trait_mapping.py", line 313, in test_predict_all_traits
    results = self.scientific_model.predict_all_traits(comprehensive_data)
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\trait_mapping\scientific_models.py", line 483, in predict_all_traits
    results['metadata']['prediction_timestamp'] = np.datetime64('now').isoformat()
                                                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: 'numpy.datetime64' object has no attribute 'isoformat'

======================================================================
ERROR: test_map_session_traits_comprehensive (tests.test_trait_mapping.TestTraitMapper.test_map_session_traits_comprehensive)       
Test comprehensive trait mapping for a session.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_trait_mapping.py", line 34, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status'

======================================================================
ERROR: test_map_traits_insufficient_metrics (tests.test_trait_mapping.TestTraitMapper.test_map_traits_insufficient_metrics)
Test trait mapping with insufficient metrics.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_trait_mapping.py", line 34, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status'

======================================================================
ERROR: test_normalization_methods (tests.test_trait_mapping.TestTraitMapper.test_normalization_methods)
Test different normalization methods.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_trait_mapping.py", line 34, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status'

======================================================================
ERROR: test_trait_explanation_generation (tests.test_trait_mapping.TestTraitMapper.test_trait_explanation_generation)
Test generation of trait explanations.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_trait_mapping.py", line 34, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status'

======================================================================
ERROR: test_weight_functions (tests.test_trait_mapping.TestTraitMapper.test_weight_functions)
Test different weight functions.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_trait_mapping.py", line 34, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status'

======================================================================
ERROR: test_outlier_detection (tests.test_trait_mapping.TestTraitValidation.test_outlier_detection)
Test outlier detection in metrics.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_trait_mapping.py", line 361, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status', 'duration_ms'

======================================================================
ERROR: test_temporal_stability_validation (tests.test_trait_mapping.TestTraitValidation.test_temporal_stability_validation)
Test temporal stability validation.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_trait_mapping.py", line 361, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status', 'duration_ms'

======================================================================
ERROR: test_validate_low_quality_data (tests.test_trait_mapping.TestTraitValidation.test_validate_low_quality_data)
Test validation with low quality data.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_trait_mapping.py", line 361, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status', 'duration_ms'

======================================================================
ERROR: test_validate_trait_profile_comprehensive (tests.test_trait_mapping.TestTraitValidation.test_validate_trait_profile_comprehensive)
Test comprehensive trait profile validation.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_trait_mapping.py", line 361, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status', 'duration_ms'

======================================================================
ERROR: test_validation_summary (tests.test_trait_mapping.TestTraitValidation.test_validation_summary)
Test validation summary functionality.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_trait_mapping.py", line 361, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status', 'duration_ms'

======================================================================
FAIL: test_unauthenticated_access (tests.test_api.TestAPIAuthentication.test_unauthenticated_access)
Test that unauthenticated requests are rejected.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_api.py", line 436, in test_unauthenticated_access      
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
AssertionError: 403 != 401

======================================================================
FAIL: test_export_import_configuration (tests.test_config.TestSettingsManager.test_export_import_configuration)
Test exporting and importing configuration.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_config.py", line 217, in test_export_import_configuration
    self.assertEqual(
AssertionError: 180 != 365

======================================================================
FAIL: test_get_nested_configuration_values (tests.test_config.TestSettingsManager.test_get_nested_configuration_values)
Test getting nested configuration values using dot notation.      
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_config.py", line 90, in test_get_nested_configuration_values
    self.assertIsNone(
AssertionError: 'default_value' is not None

======================================================================
FAIL: test_load_configuration_from_file (tests.test_config.TestSettingsManager.test_load_configuration_from_file)
Test loading configuration from file.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_config.py", line 64, in test_load_configuration_from_file
    self.assertEqual(
AssertionError: 180 != 365

----------------------------------------------------------------------
Ran 79 tests in 4.829s

FAILED (failures=4, errors=42)
Destroying test database for alias 'default' ('file:memorydb_default?mode=memory&cache=shared')...

================================================================================
TEST SUMMARY
================================================================================
❌ SOME TESTS FAILED!

Overall Status: 💥 FAILURE

================================================================================

🔧 RECOMMENDATIONS:
1. Review failed test output above
2. Check database migrations are up to date
3. Verify all dependencies are installed
4. Ensure Redis is running for Celery tests
5. Check Django settings configuration


===========================================================


  tests    python run_tests.py --agents

🤖 Running Agent Tests...

Running tests for module: tests.test_agents
--------------------------------------------------
Found 14 test(s).                                                 
Creating test database for alias 'default' ('file:memorydb_default?mode=memory&cache=shared')...
Operations to perform:
  Synchronize unmigrated apps: messages, rest_framework, staticfiles, widget_tweaks
  Apply all migrations: accounts, admin, ai_model, auth, behavioral_data, contenttypes, games, sessions
Synchronizing apps without migrations:
  Creating tables...
    Running deferred SQL...
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying contenttypes.0002_remove_content_type_name... OK       
  Applying auth.0001_initial... OK
  Applying auth.0002_alter_permission_name_max_length... OK       
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK    
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK        
  Applying auth.0010_alter_group_name_max_length... OK
  Applying auth.0011_update_proxy_permissions... OK
  Applying auth.0012_alter_user_first_name_max_length... OK       
  Applying accounts.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying games.0001_initial... OK
  Applying ai_model.0001_initial... OK
  Applying ai_model.0002_assessmentvalidation_successmodel_traitassessment_and_more... OK
  Applying behavioral_data.0001_initial... OK
  Applying games.0002_alter_gameresult_game_type... OK
  Applying sessions.0001_initial... OK
System check identified no issues (0 silenced).
test_complete_workflow (tests.test_agents.TestAgentIntegration.test_complete_workflow)
Test complete workflow from event logging to report generation. ... INFO Agent event_logger initialized with config: {}
INFO Agent metric_extractor initialized with config: {}
INFO Agent trait_inferencer initialized with config: {}
INFO Agent report_generator initialized with config: {}
ERROR
test_batch_event_logging (tests.test_agents.TestEventLogger.test_batch_event_logging)
Test batch logging of multiple events. ... INFO Agent event_logger initialized with config: {}
ERROR
test_log_event_invalid_session (tests.test_agents.TestEventLogger.test_log_event_invalid_session)
Test logging an event with invalid session ID. ... INFO Agent event_logger initialized with config: {}
ERROR
test_log_invalid_event_missing_required_field (tests.test_agents.TestEventLogger.test_log_invalid_event_missing_required_field)     
Test logging an event with missing required fields. ... INFO Agent event_logger initialized with config: {}
ERROR
test_log_valid_balloon_risk_event (tests.test_agents.TestEventLogger.test_log_valid_balloon_risk_event)
Test logging a valid balloon risk event. ... INFO Agent event_logger initialized with config: {}
ERROR
test_batch_metric_extraction (tests.test_agents.TestMetricExtractor.test_batch_metric_extraction)
Test batch extraction of metrics for multiple sessions. ... INFO Agent metric_extractor initialized with config: {}
ERROR
test_extract_balloon_risk_metrics (tests.test_agents.TestMetricExtractor.test_extract_balloon_risk_metrics)
Test extraction of balloon risk metrics. ... INFO Agent metric_extractor initialized with config: {}
ERROR
test_extract_metrics_insufficient_data (tests.test_agents.TestMetricExtractor.test_extract_metrics_insufficient_data)
Test metric extraction with insufficient data. ... INFO Agent metric_extractor initialized with config: {}
ERROR
test_generate_comparative_report (tests.test_agents.TestReportGenerator.test_generate_comparative_report)
Test generation of comparative report. ... INFO Agent report_generator initialized with config: {}
ERROR
test_generate_report_no_traits (tests.test_agents.TestReportGenerator.test_generate_report_no_traits)
Test report generation for session without trait profiles. ... INFO Agent report_generator initialized with config: {}
ERROR
test_generate_session_report (tests.test_agents.TestReportGenerator.test_generate_session_report)
Test generation of session report. ... INFO Agent report_generator initialized with config: {}
ERROR
test_infer_session_traits (tests.test_agents.TestTraitInferencer.test_infer_session_traits)
Test trait inference for a session. ... INFO Agent trait_inferencer initialized with config: {}
ERROR
test_infer_traits_insufficient_metrics (tests.test_agents.TestTraitInferencer.test_infer_traits_insufficient_metrics)
Test trait inference with insufficient metrics. ... INFO Agent trait_inferencer initialized with config: {}
ERROR
test_validate_trait_profile (tests.test_agents.TestTraitInferencer.test_validate_trait_profile)
Test trait profile validation. ... INFO Agent trait_inferencer initialized with config: {}
ERROR

======================================================================
ERROR: test_complete_workflow (tests.test_agents.TestAgentIntegration.test_complete_workflow)
Test complete workflow from event logging to report generation.   
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_agents.py", line 516, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status'

======================================================================
ERROR: test_batch_event_logging (tests.test_agents.TestEventLogger.test_batch_event_logging)
Test batch logging of multiple events.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_agents.py", line 32, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status'

======================================================================
ERROR: test_log_event_invalid_session (tests.test_agents.TestEventLogger.test_log_event_invalid_session)
Test logging an event with invalid session ID.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_agents.py", line 32, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status'

======================================================================
ERROR: test_log_invalid_event_missing_required_field (tests.test_agents.TestEventLogger.test_log_invalid_event_missing_required_field)
Test logging an event with missing required fields.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_agents.py", line 32, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status'

======================================================================
ERROR: test_log_valid_balloon_risk_event (tests.test_agents.TestEventLogger.test_log_valid_balloon_risk_event)
Test logging a valid balloon risk event.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_agents.py", line 32, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status'

======================================================================
ERROR: test_batch_metric_extraction (tests.test_agents.TestMetricExtractor.test_batch_metric_extraction)
Test batch extraction of metrics for multiple sessions.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_agents.py", line 128, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status', 'duration_ms'

======================================================================
ERROR: test_extract_balloon_risk_metrics (tests.test_agents.TestMetricExtractor.test_extract_balloon_risk_metrics)
Test extraction of balloon risk metrics.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_agents.py", line 128, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status', 'duration_ms'

======================================================================
ERROR: test_extract_metrics_insufficient_data (tests.test_agents.TestMetricExtractor.test_extract_metrics_insufficient_data)        
Test metric extraction with insufficient data.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_agents.py", line 128, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status', 'duration_ms'

======================================================================
ERROR: test_generate_comparative_report (tests.test_agents.TestReportGenerator.test_generate_comparative_report)
Test generation of comparative report.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_agents.py", line 395, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status', 'duration_ms'

======================================================================
ERROR: test_generate_report_no_traits (tests.test_agents.TestReportGenerator.test_generate_report_no_traits)
Test report generation for session without trait profiles.        
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_agents.py", line 395, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status', 'duration_ms'

======================================================================
ERROR: test_generate_session_report (tests.test_agents.TestReportGenerator.test_generate_session_report)
Test generation of session report.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_agents.py", line 395, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status', 'duration_ms'

======================================================================
ERROR: test_infer_session_traits (tests.test_agents.TestTraitInferencer.test_infer_session_traits)
Test trait inference for a session.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_agents.py", line 277, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status'

======================================================================
ERROR: test_infer_traits_insufficient_metrics (tests.test_agents.TestTraitInferencer.test_infer_traits_insufficient_metrics)        
Test trait inference with insufficient metrics.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_agents.py", line 277, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status'

======================================================================
ERROR: test_validate_trait_profile (tests.test_agents.TestTraitInferencer.test_validate_trait_profile)
Test trait profile validation.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_agents.py", line 277, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status'

----------------------------------------------------------------------
Ran 14 tests in 0.025s

FAILED (errors=14)
Destroying test database for alias 'default' ('file:memorydb_default?mode=memory&cache=shared')...


==============================================================
  tests    python run_tests.py --traits

🧠 Running Trait Mapping Tests...

Running tests for module: tests.test_trait_mapping
--------------------------------------------------
Found 16 test(s).
Creating test database for alias 'default' ('file:memorydb_default?mode=memory&cache=shared')...
Operations to perform:
  Synchronize unmigrated apps: messages, rest_framework, staticfiles, widget_tweaks
  Apply all migrations: accounts, admin, ai_model, auth, behavioral_data, contenttypes, games, sessions
Synchronizing apps without migrations:
  Creating tables...
    Running deferred SQL...
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying contenttypes.0002_remove_content_type_name... OK       
  Applying auth.0001_initial... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK    
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK        
  Applying auth.0010_alter_group_name_max_length... OK
  Applying auth.0011_update_proxy_permissions... OK
  Applying auth.0012_alter_user_first_name_max_length... OK       
  Applying accounts.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying games.0001_initial... OK
  Applying ai_model.0001_initial... OK
  Applying ai_model.0002_assessmentvalidation_successmodel_traitassessment_and_more... OK
  Applying behavioral_data.0001_initial... OK
  Applying games.0002_alter_gameresult_game_type... OK
  Applying sessions.0001_initial... OK
System check identified no issues (0 silenced).
test_confidence_intervals (tests.test_trait_mapping.TestScientificTraitModel.test_confidence_intervals)
Test confidence interval calculations. ... ok
test_emotion_regulation_model_prediction (tests.test_trait_mapping.TestScientificTraitModel.test_emotion_regulation_model_prediction)
Test emotion regulation model prediction. ... ok
test_learning_ability_model_prediction (tests.test_trait_mapping.TestScientificTraitModel.test_learning_ability_model_prediction)   
Test learning ability model prediction. ... ok
test_model_validation (tests.test_trait_mapping.TestScientificTraitModel.test_model_validation)
Test model validation functionality. ... ok
test_predict_all_traits (tests.test_trait_mapping.TestScientificTraitModel.test_predict_all_traits)
Test prediction of all traits using scientific models. ... ERROR  
test_risk_tolerance_model_prediction (tests.test_trait_mapping.TestScientificTraitModel.test_risk_tolerance_model_prediction)       
Test risk tolerance model prediction. ... ok
test_map_session_traits_comprehensive (tests.test_trait_mapping.TestTraitMapper.test_map_session_traits_comprehensive)
Test comprehensive trait mapping for a session. ... ERROR
test_map_traits_insufficient_metrics (tests.test_trait_mapping.TestTraitMapper.test_map_traits_insufficient_metrics)
Test trait mapping with insufficient metrics. ... ERROR
test_normalization_methods (tests.test_trait_mapping.TestTraitMapper.test_normalization_methods)
Test different normalization methods. ... ERROR
test_trait_explanation_generation (tests.test_trait_mapping.TestTraitMapper.test_trait_explanation_generation)
Test generation of trait explanations. ... ERROR
test_weight_functions (tests.test_trait_mapping.TestTraitMapper.test_weight_functions)
Test different weight functions. ... ERROR
test_outlier_detection (tests.test_trait_mapping.TestTraitValidation.test_outlier_detection)
Test outlier detection in metrics. ... ERROR
test_temporal_stability_validation (tests.test_trait_mapping.TestTraitValidation.test_temporal_stability_validation)
Test temporal stability validation. ... ERROR
test_validate_low_quality_data (tests.test_trait_mapping.TestTraitValidation.test_validate_low_quality_data)
Test validation with low quality data. ... ERROR
test_validate_trait_profile_comprehensive (tests.test_trait_mapping.TestTraitValidation.test_validate_trait_profile_comprehensive)  
Test comprehensive trait profile validation. ... ERROR
test_validation_summary (tests.test_trait_mapping.TestTraitValidation.test_validation_summary)
Test validation summary functionality. ... ERROR

======================================================================
ERROR: test_predict_all_traits (tests.test_trait_mapping.TestScientificTraitModel.test_predict_all_traits)
Test prediction of all traits using scientific models.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_trait_mapping.py", line 313, in test_predict_all_traits
    results = self.scientific_model.predict_all_traits(comprehensive_data)
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\trait_mapping\scientific_models.py", line 483, in predict_all_traits
    results['metadata']['prediction_timestamp'] = np.datetime64('now').isoformat()
                                                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: 'numpy.datetime64' object has no attribute 'isoformat'

======================================================================
ERROR: test_map_session_traits_comprehensive (tests.test_trait_mapping.TestTraitMapper.test_map_session_traits_comprehensive)       
Test comprehensive trait mapping for a session.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_trait_mapping.py", line 34, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status'

======================================================================
ERROR: test_map_traits_insufficient_metrics (tests.test_trait_mapping.TestTraitMapper.test_map_traits_insufficient_metrics)
Test trait mapping with insufficient metrics.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_trait_mapping.py", line 34, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status'

======================================================================
ERROR: test_normalization_methods (tests.test_trait_mapping.TestTraitMapper.test_normalization_methods)
Test different normalization methods.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_trait_mapping.py", line 34, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status'

======================================================================
ERROR: test_trait_explanation_generation (tests.test_trait_mapping.TestTraitMapper.test_trait_explanation_generation)
Test generation of trait explanations.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_trait_mapping.py", line 34, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status'

======================================================================
ERROR: test_weight_functions (tests.test_trait_mapping.TestTraitMapper.test_weight_functions)
Test different weight functions.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_trait_mapping.py", line 34, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status'

======================================================================
ERROR: test_outlier_detection (tests.test_trait_mapping.TestTraitValidation.test_outlier_detection)
Test outlier detection in metrics.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_trait_mapping.py", line 361, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status', 'duration_ms'

======================================================================
ERROR: test_temporal_stability_validation (tests.test_trait_mapping.TestTraitValidation.test_temporal_stability_validation)
Test temporal stability validation.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_trait_mapping.py", line 361, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status', 'duration_ms'

======================================================================
ERROR: test_validate_low_quality_data (tests.test_trait_mapping.TestTraitValidation.test_validate_low_quality_data)
Test validation with low quality data.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_trait_mapping.py", line 361, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status', 'duration_ms'

======================================================================
ERROR: test_validate_trait_profile_comprehensive (tests.test_trait_mapping.TestTraitValidation.test_validate_trait_profile_comprehensive)
Test comprehensive trait profile validation.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_trait_mapping.py", line 361, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status', 'duration_ms'

======================================================================
ERROR: test_validation_summary (tests.test_trait_mapping.TestTraitValidation.test_validation_summary)
Test validation summary functionality.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_trait_mapping.py", line 361, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status', 'duration_ms'

----------------------------------------------------------------------
Ran 16 tests in 0.028s

FAILED (errors=11)
Destroying test database for alias 'default' ('file:memorydb_default?mode=memory&cache=shared')...

==============================================================


  tests    python run_tests.py --api

🌐 Running API Tests...
                                                                  Running tests for module: tests.test_api                          
--------------------------------------------------
Found 22 test(s).                                                 
Creating test database for alias 'default' ('file:memorydb_default?mode=memory&cache=shared')...
Operations to perform:
  Synchronize unmigrated apps: messages, rest_framework, staticfiles, widget_tweaks
  Apply all migrations: accounts, admin, ai_model, auth, behavioral_data, contenttypes, games, sessions
Synchronizing apps without migrations:
  Creating tables...
    Running deferred SQL...
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying contenttypes.0002_remove_content_type_name... OK       
  Applying auth.0001_initial... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK    
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying auth.0010_alter_group_name_max_length... OK
  Applying auth.0011_update_proxy_permissions... OK
  Applying auth.0012_alter_user_first_name_max_length... OK       
  Applying accounts.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK      
  Applying games.0001_initial... OK
  Applying ai_model.0001_initial... OK
  Applying ai_model.0002_assessmentvalidation_successmodel_traitassessment_and_more... OK
  Applying behavioral_data.0001_initial... OK
  Applying games.0002_alter_gameresult_game_type... OK
  Applying sessions.0001_initial... OK
System check identified no issues (0 silenced).
test_authenticated_access (tests.test_api.TestAPIAuthentication.test_authenticated_access)
Test that authenticated requests are allowed. ... ok
test_session_authentication (tests.test_api.TestAPIAuthentication.test_session_authentication)
Test session-based authentication. ... ok
test_unauthenticated_access (tests.test_api.TestAPIAuthentication.test_unauthenticated_access)
Test that unauthenticated requests are rejected. ... WARNING Forbidden: /api/sessions/
FAIL
test_invalid_json_request (tests.test_api.TestAPIErrorHandling.test_invalid_json_request)
Test handling of invalid JSON requests. ... WARNING Bad Request: /api/sessions/
ok
test_missing_required_fields (tests.test_api.TestAPIErrorHandling.test_missing_required_fields)
Test handling of requests with missing required fields. ... WARNING Bad Request: /api/sessions/
ok
test_nonexistent_resource (tests.test_api.TestAPIErrorHandling.test_nonexistent_resource)
Test handling of requests for nonexistent resources. ... WARNING Not Found: /api/sessions/99999/
ok
test_bulk_session_listing_performance (tests.test_api.TestAPIPerformance.test_bulk_session_listing_performance)
Test performance of listing many sessions. ... ERROR
test_pagination_functionality (tests.test_api.TestAPIPerformance.test_pagination_functionality)
Test API pagination functionality. ... ERROR
test_create_behavioral_event (tests.test_api.TestBehavioralDataAPI.test_create_behavioral_event)
Test creating behavioral events via API. ... ERROR
test_create_behavioral_session (tests.test_api.TestBehavioralDataAPI.test_create_behavioral_session)
Test creating a new behavioral session via API. ... ERROR
test_create_invalid_behavioral_event (tests.test_api.TestBehavioralDataAPI.test_create_invalid_behavioral_event)
Test creating invalid behavioral event via API. ... ERROR
test_list_behavioral_events (tests.test_api.TestBehavioralDataAPI.test_list_behavioral_events)
Test listing behavioral events via API. ... ERROR
test_list_behavioral_sessions (tests.test_api.TestBehavioralDataAPI.test_list_behavioral_sessions)
Test listing behavioral sessions via API. ... ERROR
test_retrieve_behavioral_session (tests.test_api.TestBehavioralDataAPI.test_retrieve_behavioral_session)
Test retrieving a specific behavioral session via API. ... ERROR  
test_extract_metrics_api (tests.test_api.TestMetricExtractionAPI.test_extract_metrics_api)
Test metric extraction via API. ... ERROR
test_extract_metrics_invalid_session (tests.test_api.TestMetricExtractionAPI.test_extract_metrics_invalid_session)
Test metric extraction with invalid session ID. ... ERROR
test_list_behavioral_metrics (tests.test_api.TestMetricExtractionAPI.test_list_behavioral_metrics)
Test listing behavioral metrics via API. ... ERROR
test_generate_report_api (tests.test_api.TestReportGenerationAPI.test_generate_report_api)
Test report generation via API. ... ERROR
test_generate_report_invalid_session (tests.test_api.TestReportGenerationAPI.test_generate_report_invalid_session)
Test report generation with invalid session ID. ... ERROR
test_create_trait_profile (tests.test_api.TestTraitInferenceAPI.test_create_trait_profile)
Test creating trait profile via API. ... ERROR
test_infer_traits_api (tests.test_api.TestTraitInferenceAPI.test_infer_traits_api)
Test trait inference via API. ... ERROR
test_list_trait_profiles (tests.test_api.TestTraitInferenceAPI.test_list_trait_profiles)
Test listing trait profiles via API. ... ERROR

======================================================================
ERROR: test_bulk_session_listing_performance (tests.test_api.TestAPIPerformance.test_bulk_session_listing_performance)
Test performance of listing many sessions.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_api.py", line 519, in setUp
    self._create_bulk_test_data()
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_api.py", line 525, in _create_bulk_test_data
    session = BehavioralSession(
              ^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status'

======================================================================
ERROR: test_pagination_functionality (tests.test_api.TestAPIPerformance.test_pagination_functionality)
Test API pagination functionality.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_api.py", line 519, in setUp
    self._create_bulk_test_data()
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_api.py", line 525, in _create_bulk_test_data
    session = BehavioralSession(
              ^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status'

======================================================================
ERROR: test_create_behavioral_event (tests.test_api.TestBehavioralDataAPI.test_create_behavioral_event)
Test creating behavioral events via API.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_api.py", line 41, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status'

======================================================================
ERROR: test_create_behavioral_session (tests.test_api.TestBehavioralDataAPI.test_create_behavioral_session)
Test creating a new behavioral session via API.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_api.py", line 41, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status'

======================================================================
ERROR: test_create_invalid_behavioral_event (tests.test_api.TestBehavioralDataAPI.test_create_invalid_behavioral_event)
Test creating invalid behavioral event via API.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_api.py", line 41, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status'

======================================================================
ERROR: test_list_behavioral_events (tests.test_api.TestBehavioralDataAPI.test_list_behavioral_events)
Test listing behavioral events via API.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_api.py", line 41, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status'

======================================================================
ERROR: test_list_behavioral_sessions (tests.test_api.TestBehavioralDataAPI.test_list_behavioral_sessions)
Test listing behavioral sessions via API.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_api.py", line 41, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status'

======================================================================
ERROR: test_retrieve_behavioral_session (tests.test_api.TestBehavioralDataAPI.test_retrieve_behavioral_session)
Test retrieving a specific behavioral session via API.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_api.py", line 41, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status'

======================================================================
ERROR: test_extract_metrics_api (tests.test_api.TestMetricExtractionAPI.test_extract_metrics_api)
Test metric extraction via API.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_api.py", line 160, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status'

======================================================================
ERROR: test_extract_metrics_invalid_session (tests.test_api.TestMetricExtractionAPI.test_extract_metrics_invalid_session)
Test metric extraction with invalid session ID.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_api.py", line 160, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status'

======================================================================
ERROR: test_list_behavioral_metrics (tests.test_api.TestMetricExtractionAPI.test_list_behavioral_metrics)
Test listing behavioral metrics via API.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_api.py", line 160, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status'

======================================================================
ERROR: test_generate_report_api (tests.test_api.TestReportGenerationAPI.test_generate_report_api)
Test report generation via API.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_api.py", line 356, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status', 'duration_ms'

======================================================================
ERROR: test_generate_report_invalid_session (tests.test_api.TestReportGenerationAPI.test_generate_report_invalid_session)
Test report generation with invalid session ID.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_api.py", line 356, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status', 'duration_ms'

======================================================================
ERROR: test_create_trait_profile (tests.test_api.TestTraitInferenceAPI.test_create_trait_profile)
Test creating trait profile via API.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_api.py", line 251, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status'

======================================================================
ERROR: test_infer_traits_api (tests.test_api.TestTraitInferenceAPI.test_infer_traits_api)
Test trait inference via API.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_api.py", line 251, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status'

======================================================================
ERROR: test_list_trait_profiles (tests.test_api.TestTraitInferenceAPI.test_list_trait_profiles)
Test listing trait profiles via API.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_api.py", line 251, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status'

======================================================================
FAIL: test_unauthenticated_access (tests.test_api.TestAPIAuthentication.test_unauthenticated_access)
Test that unauthenticated requests are rejected.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_api.py", line 436, in test_unauthenticated_access      
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
AssertionError: 403 != 401

----------------------------------------------------------------------
Ran 22 tests in 4.431s

FAILED (failures=1, errors=16)
Destroying test database for alias 'default' ('file:memorydb_default?mode=memory&cache=shared')...


==============================================================


tests\test_agents.py", line 277, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status'

======================================================================
ERROR: test_infer_traits_insufficient_metrics (tests.test_agents.TestTraitInferencer.test_infer_traits_insufficient_metrics)        
Test trait inference with insufficient metrics.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_agents.py", line 277, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status'

======================================================================
ERROR: test_validate_trait_profile (tests.test_agents.TestTraitInferencer.test_validate_trait_profile)
Test trait profile validation.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_agents.py", line 277, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status'

======================================================================
ERROR: test_bulk_session_listing_performance (tests.test_api.TestAPIPerformance.test_bulk_session_listing_performance)
Test performance of listing many sessions.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_api.py", line 519, in setUp
    self._create_bulk_test_data()
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_api.py", line 525, in _create_bulk_test_data
    session = BehavioralSession(
              ^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status'

======================================================================
ERROR: test_pagination_functionality (tests.test_api.TestAPIPerformance.test_pagination_functionality)
Test API pagination functionality.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_api.py", line 519, in setUp
    self._create_bulk_test_data()
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_api.py", line 525, in _create_bulk_test_data
    session = BehavioralSession(
              ^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status'

======================================================================
ERROR: test_create_behavioral_event (tests.test_api.TestBehavioralDataAPI.test_create_behavioral_event)
Test creating behavioral events via API.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_api.py", line 41, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status'

======================================================================
ERROR: test_create_behavioral_session (tests.test_api.TestBehavioralDataAPI.test_create_behavioral_session)
Test creating a new behavioral session via API.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_api.py", line 41, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status'

======================================================================
ERROR: test_create_invalid_behavioral_event (tests.test_api.TestBehavioralDataAPI.test_create_invalid_behavioral_event)
Test creating invalid behavioral event via API.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_api.py", line 41, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status'

======================================================================
ERROR: test_list_behavioral_events (tests.test_api.TestBehavioralDataAPI.test_list_behavioral_events)
Test listing behavioral events via API.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_api.py", line 41, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status'

======================================================================
ERROR: test_list_behavioral_sessions (tests.test_api.TestBehavioralDataAPI.test_list_behavioral_sessions)
Test listing behavioral sessions via API.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_api.py", line 41, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status'

======================================================================
ERROR: test_retrieve_behavioral_session (tests.test_api.TestBehavioralDataAPI.test_retrieve_behavioral_session)
Test retrieving a specific behavioral session via API.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_api.py", line 41, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status'

======================================================================
ERROR: test_extract_metrics_api (tests.test_api.TestMetricExtractionAPI.test_extract_metrics_api)
Test metric extraction via API.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_api.py", line 160, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status'

======================================================================
ERROR: test_extract_metrics_invalid_session (tests.test_api.TestMetricExtractionAPI.test_extract_metrics_invalid_session)
Test metric extraction with invalid session ID.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_api.py", line 160, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status'

======================================================================
ERROR: test_list_behavioral_metrics (tests.test_api.TestMetricExtractionAPI.test_list_behavioral_metrics)
Test listing behavioral metrics via API.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_api.py", line 160, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status'

======================================================================
ERROR: test_generate_report_api (tests.test_api.TestReportGenerationAPI.test_generate_report_api)
Test report generation via API.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_api.py", line 356, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status', 'duration_ms'

======================================================================
ERROR: test_generate_report_invalid_session (tests.test_api.TestReportGenerationAPI.test_generate_report_invalid_session)
Test report generation with invalid session ID.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_api.py", line 356, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status', 'duration_ms'

======================================================================
ERROR: test_create_trait_profile (tests.test_api.TestTraitInferenceAPI.test_create_trait_profile)
Test creating trait profile via API.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_api.py", line 251, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status'

======================================================================
ERROR: test_infer_traits_api (tests.test_api.TestTraitInferenceAPI.test_infer_traits_api)
Test trait inference via API.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_api.py", line 251, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status'

======================================================================
ERROR: test_list_trait_profiles (tests.test_api.TestTraitInferenceAPI.test_list_trait_profiles)
Test listing trait profiles via API.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_api.py", line 251, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status'

======================================================================
ERROR: test_predict_all_traits (tests.test_trait_mapping.TestScientificTraitModel.test_predict_all_traits)
Test prediction of all traits using scientific models.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_trait_mapping.py", line 313, in test_predict_all_traits
    results = self.scientific_model.predict_all_traits(comprehensive_data)
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\trait_mapping\scientific_models.py", line 483, in predict_all_traits
    results['metadata']['prediction_timestamp'] = np.datetime64('now').isoformat()
                                                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: 'numpy.datetime64' object has no attribute 'isoformat'

======================================================================
ERROR: test_map_session_traits_comprehensive (tests.test_trait_mapping.TestTraitMapper.test_map_session_traits_comprehensive)       
Test comprehensive trait mapping for a session.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_trait_mapping.py", line 34, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status'

======================================================================
ERROR: test_map_traits_insufficient_metrics (tests.test_trait_mapping.TestTraitMapper.test_map_traits_insufficient_metrics)
Test trait mapping with insufficient metrics.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_trait_mapping.py", line 34, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status'

======================================================================
ERROR: test_normalization_methods (tests.test_trait_mapping.TestTraitMapper.test_normalization_methods)
Test different normalization methods.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_trait_mapping.py", line 34, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status'

======================================================================
ERROR: test_trait_explanation_generation (tests.test_trait_mapping.TestTraitMapper.test_trait_explanation_generation)
Test generation of trait explanations.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_trait_mapping.py", line 34, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status'

======================================================================
ERROR: test_weight_functions (tests.test_trait_mapping.TestTraitMapper.test_weight_functions)
Test different weight functions.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_trait_mapping.py", line 34, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status'

======================================================================
ERROR: test_outlier_detection (tests.test_trait_mapping.TestTraitValidation.test_outlier_detection)
Test outlier detection in metrics.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_trait_mapping.py", line 361, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status', 'duration_ms'

======================================================================
ERROR: test_temporal_stability_validation (tests.test_trait_mapping.TestTraitValidation.test_temporal_stability_validation)
Test temporal stability validation.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_trait_mapping.py", line 361, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status', 'duration_ms'

======================================================================
ERROR: test_validate_low_quality_data (tests.test_trait_mapping.TestTraitValidation.test_validate_low_quality_data)
Test validation with low quality data.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_trait_mapping.py", line 361, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status', 'duration_ms'

======================================================================
ERROR: test_validate_trait_profile_comprehensive (tests.test_trait_mapping.TestTraitValidation.test_validate_trait_profile_comprehensive)
Test comprehensive trait profile validation.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_trait_mapping.py", line 361, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status', 'duration_ms'

======================================================================
ERROR: test_validation_summary (tests.test_trait_mapping.TestTraitValidation.test_validation_summary)
Test validation summary functionality.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_trait_mapping.py", line 361, in setUp
    self.test_session = BehavioralSession.objects.create(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)    
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\query.py", line 675, in create
    obj = self.model(**kwargs)
          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\MSI\miniconda3\Lib\site-packages\django\db\models\base.py", line 567, in __init__
    raise TypeError(
TypeError: BehavioralSession() got unexpected keyword arguments: 'game_type', 'started_at', 'status', 'duration_ms'

======================================================================
FAIL: test_unauthenticated_access (tests.test_api.TestAPIAuthentication.test_unauthenticated_access)
Test that unauthenticated requests are rejected.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_api.py", line 436, in test_unauthenticated_access      
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
AssertionError: 403 != 401

======================================================================
FAIL: test_export_import_configuration (tests.test_config.TestSettingsManager.test_export_import_configuration)
Test exporting and importing configuration.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_config.py", line 217, in test_export_import_configuration
    self.assertEqual(
AssertionError: 180 != 365

======================================================================
FAIL: test_get_nested_configuration_values (tests.test_config.TestSettingsManager.test_get_nested_configuration_values)
Test getting nested configuration values using dot notation.      
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_config.py", line 90, in test_get_nested_configuration_values
    self.assertIsNone(
AssertionError: 'default_value' is not None

======================================================================
FAIL: test_load_configuration_from_file (tests.test_config.TestSettingsManager.test_load_configuration_from_file)
Test loading configuration from file.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\django_project\deepseekdjango\django_pymetrics_crs_end\tests\test_config.py", line 64, in test_load_configuration_from_file
    self.assertEqual(
AssertionError: 180 != 365

----------------------------------------------------------------------
Ran 79 tests in 4.321s

FAILED (failures=4, errors=42)
Destroying test database for alias 'default'...

================================================================================
TEST SUMMARY
================================================================================
❌ SOME TESTS FAILED!

Overall Status: 💥 FAILURE

================================================================================

🔧 RECOMMENDATIONS:
1. Review failed test output above
2. Check database migrations are up to date
3. Verify all dependencies are installed
4. Ensure Redis is running for Celery tests
5. Check Django settings configuration

Coverage Report:
Name                                                              
                                                                  
               Stmts   Miss  Cover
----------------------------------------------------------------------------------------------------------------------------------------------------------------------
D:\django_project\deepseekdjango\django_pymetrics_crs_end\accounts\forms.py                                                         
                  33      6    82%
D:\django_project\deepseekdjango\django_pymetrics_crs_end\accounts\migrations\0001_initial.py                                       
                  10      0   100%
D:\django_project\deepseekdjango\django_pymetrics_crs_end\accounts\migrations\__init__.py                                           
                   0      0   100%
D:\django_project\deepseekdjango\django_pymetrics_crs_end\accounts\urls.py                                                          
                   3      0   100%
D:\django_project\deepseekdjango\django_pymetrics_crs_end\accounts\views.py                                                         
                 213    168    21%
D:\django_project\deepseekdjango\django_pymetrics_crs_end\agents\__init__.py                                                        
                   1      0   100%
D:\django_project\deepseekdjango\django_pymetrics_crs_end\agents\base_agent.py                                                      
                 125     68    46%
D:\django_project\deepseekdjango\django_pymetrics_crs_end\agents\event_logger.py                                                    
                 139    109    22%
D:\django_project\deepseekdjango\django_pymetrics_crs_end\agents\metric_extractor.py                                                
                 187    149    20%
D:\django_project\deepseekdjango\django_pymetrics_crs_end\agents\report_generator.py                                                
                 249    202    19%
D:\django_project\deepseekdjango\django_pymetrics_crs_end\agents\trait_inferencer.py                                                
                 267    225    16%
D:\django_project\deepseekdjango\django_pymetrics_crs_end\ai_model\api_views.py                                                     
                  11      5    55%
D:\django_project\deepseekdjango\django_pymetrics_crs_end\ai_model\migrations\0001_initial.py                                       
                   6      0   100%
D:\django_project\deepseekdjango\django_pymetrics_crs_end\ai_model\migrations\0002_assessmentvalidation_successmodel_traitassessment_and_more.py       9      0   100%
D:\django_project\deepseekdjango\django_pymetrics_crs_end\ai_model\migrations\__init__.py                                           
                   0      0   100%
D:\django_project\deepseekdjango\django_pymetrics_crs_end\ai_model\serializers.py                                                   
                  18      0   100%
D:\django_project\deepseekdjango\django_pymetrics_crs_end\ai_model\urls.py                                                          
                   9      0   100%
D:\django_project\deepseekdjango\django_pymetrics_crs_end\ai_model\views.py                                                         
                  40     10    75%
D:\django_project\deepseekdjango\django_pymetrics_crs_end\api\serializers.py                                                        
                  19      0   100%
D:\django_project\deepseekdjango\django_pymetrics_crs_end\api\urls.py                                                               
                  11      0   100%
D:\django_project\deepseekdjango\django_pymetrics_crs_end\api\views.py                                                              
                  41     12    71%
D:\django_project\deepseekdjango\django_pymetrics_crs_end\behavioral_data\api_views.py                                              
                  11      5    55%
D:\django_project\deepseekdjango\django_pymetrics_crs_end\behavioral_data\migrations\0001_initial.py                                
                   9      0   100%
D:\django_project\deepseekdjango\django_pymetrics_crs_end\behavioral_data\migrations\__init__.py                                    
                   0      0   100%
D:\django_project\deepseekdjango\django_pymetrics_crs_end\behavioral_data\schemas.py                                                
                 259    227    12%
D:\django_project\deepseekdjango\django_pymetrics_crs_end\behavioral_data\serializers.py                                            
                  26      0   100%
D:\django_project\deepseekdjango\django_pymetrics_crs_end\behavioral_data\urls.py                                                   
                  11      0   100%
D:\django_project\deepseekdjango\django_pymetrics_crs_end\behavioral_data\validators.py                                             
                 202    162    20%
D:\django_project\deepseekdjango\django_pymetrics_crs_end\behavioral_data\views.py                                                  
                  21      0   100%
D:\django_project\deepseekdjango\django_pymetrics_crs_end\config\__init__.py                                                        
                   5      2    60%
D:\django_project\deepseekdjango\django_pymetrics_crs_end\config\scientific_config.py                                               
                 139     12    91%
D:\django_project\deepseekdjango\django_pymetrics_crs_end\config\settings_manager.py                                                
                 188     22    88%
D:\django_project\deepseekdjango\django_pymetrics_crs_end\games\migrations\0001_initial.py                                          
                   8      0   100%
D:\django_project\deepseekdjango\django_pymetrics_crs_end\games\migrations\0002_alter_gameresult_game_type.py                       
                   4      0   100%
D:\django_project\deepseekdjango\django_pymetrics_crs_end\games\migrations\__init__.py                                              
                   0      0   100%
D:\django_project\deepseekdjango\django_pymetrics_crs_end\games\urls.py                                                             
                   4      0   100%
D:\django_project\deepseekdjango\django_pymetrics_crs_end\games\views.py                                                            
                  35     20    43%
D:\django_project\deepseekdjango\django_pymetrics_crs_end\pymetric\urls.py                                                          
                  20      9    55%
D:\django_project\deepseekdjango\django_pymetrics_crs_end\tasks\__init__.py                                                         
                   1      0   100%
D:\django_project\deepseekdjango\django_pymetrics_crs_end\tasks\metric_extraction.py                                                
                   6      2    67%
D:\django_project\deepseekdjango\django_pymetrics_crs_end\tasks\reporting.py                                                        
                   6      2    67%
D:\django_project\deepseekdjango\django_pymetrics_crs_end\trait_mapping\__init__.py                                                 
                   4      0   100%
D:\django_project\deepseekdjango\django_pymetrics_crs_end\trait_mapping\scientific_models.py                                        
                 234     70    70%
D:\django_project\deepseekdjango\django_pymetrics_crs_end\trait_mapping\trait_mappings.py                                           
                 177    133    25%
D:\django_project\deepseekdjango\django_pymetrics_crs_end\trait_mapping\validation.py                                               
                 224    180    20%
__init__.py                                                       
                                                                  
                   8      2    75%
run_tests.py                                                      
                                                                  
                 146    121    17%
test_agents.py                                                    
                                                                  
                 201    143    29%
test_api.py                                                       
                                                                  
                 199     97    51%
test_config.py                                                    
                                                                  
                 224      2    99%
test_trait_inference_api.py                                       
                                                                  
                  27     26     4%
test_trait_mapping.py                                             
                                                                  
                 202    116    43%
----------------------------------------------------------------------------------------------------------------------------------------------------------------------
TOTAL                                                             
                                                                  
                3992   2307    42%
HTML coverage report generated in 'htmlcov' directory

