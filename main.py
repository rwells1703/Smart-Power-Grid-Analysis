import data_load
import svc
import lp_generate
import lp_solve

def main():
    lp_generate.create_scheduling_scripts()

    # The predictions obtained from running the SVM with a high number of bagging estimators
    curves = data_load.read_data("data\\TestingData.txt", "f*")
    predictions = [1.0,1.0,0.0,0.0,1.0,1.0,0.0,1.0,1.0,0.0,0.0,0.0,1.0,0.0,0.0,1.0,1.0,1.0,1.0,1.0,0.0,1.0,0.0,0.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,0.0,1.0,0.0,0.0,1.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,1.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,1.0,1.0,0.0,1.0,0.0,0.0,0.0,0.0,1.0,1.0,0.0,0.0,1.0,1.0,1.0,0.0,0.0,0.0,1.0,0.0,0.0,1.0,1.0,1.0,1.0,1.0,1.0,0.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0.0,0.0,0.0,1.0,1.0,1.0,0.0,0.0,1.0,0.0]
    svc.save_testing_results(curves, predictions)

    #predictions, curves = svm.predict_testing_data()

    curve_indexes = svc.get_abormal_curves(predictions)
    all_hour_totals = lp_solve.get_curve_schedules(curve_indexes)
    lp_solve.display_curve_schedules(curve_indexes, all_hour_totals)
    lp_solve.graph_curve_schedules(curve_indexes, all_hour_totals)

if __name__ == "__main__":
    main()