import platform

from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist

from submission.config import Verdict, Language
from submission.models import Submission

from ddlcw import Runner as JudgeRunner
from ddl.settings import PROBLEM_TEST_CASES_DIR
import ddlcw.config


@shared_task
def run_submission_task(pk):
    try:
        submission = Submission.objects.get(id=pk)
        if platform.system() != 'Linux':
            submission.verdict = Verdict.SYSTEM_ERROR
            submission.additional_info = 'Linux platform required.'
        else:
            submission.verdict = Verdict.RUNNING
            submission.save()
            # initialize runner
            try:
                runner = JudgeRunner(PROBLEM_TEST_CASES_DIR,
                                     submission.problem.manifest,
                                     submission.problem.time_limit,
                                     submission.problem.memory_limit,
                                     submission.code,
                                     Language.LANGUAGE_CONFIG[submission.lang])
                if ddlcw.config.DEBUG:
                    print('runner')
                    print(runner.__dict__)
            except Exception as e:
                submission.additional_info = {'error': repr(e)}
                submission.verdict = Verdict.SYSTEM_ERROR
                submission.save()
                return
            # compile code
            try:
                runner.compile()
            except Exception as e:
                submission.additional_info = {'error': repr(e)}
                submission.verdict = Verdict.COMPILE_ERROR
                submission.save()
                return
            # run code
            try:
                result = runner.run()
                submission.verdict = Verdict.ACCEPTED
                # attention: time spend and memory spend indicated maximum case time spend and maximum case memory spend
                submission.time_spend = 0
                submission.memory_spend = 0
                for item in result:
                    # calculate max time spend and memory spend
                    submission.time_spend = max(submission.time_spend, item['real_time'])
                    submission.memory_spend = max(submission.memory_spend, item['memory'])
                    if item['result'] != 0:
                        submission.verdict = Verdict.VERDICT_DICT[item['result']]
                        break
                submission.additional_info = {'result': result}
                submission.save()
            except Exception as e:
                submission.additional_info = {'error': str(e)}
                submission.verdict = Verdict.SYSTEM_ERROR
                submission.save()
                return
            try:
                # clean running directory
                runner.clean()
            except OSError:
                pass
    except ObjectDoesNotExist:
        pass
