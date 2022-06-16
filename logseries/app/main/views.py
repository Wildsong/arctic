import os
from arcgis.gis import GIS
from arcgis.features import FeatureLayer
import pandas as pd
from datetime import datetime
from pytz import timezone
from tzlocal import get_localzone

from flask import render_template, redirect, flash
from flask import current_app
from . import main
from .forms import CasesForm, PPEForm

# This is for the old D3 based chart
#from csv_export import csv_exporter

# This generates a standalone HTML file
from generate_chart import generate_chart

from utils import local2utc

VERSION = 'webforms 1.4'

county_centroid = {"x": -123.74, "y": 46.09}
time_format = "%m/%d/%Y %H:%M"
error = "ERROR 99999"

def parsetime(s) :
    """ Parse a time string and return a datetime object. """
    return datetime.strptime(s, time_format)

@main.route('/fail')
def fail(e=""):
    return render_template("fail.html", error=error)

@main.route('/thanks/<df>')
def thanks(df=None):

    portal_url = current_app.config['PORTAL_URL']
    portal_user = current_app.config['PORTAL_USER']
    portal_password = current_app.config['PORTAL_PASSWORD']

    cases_url = current_app.config['COVID_CASES_URL']
    ppe_url   = current_app.config['PPE_INVENTORY_URL']

    # Show the data that was just entered.
    portal = GIS(portal_url, portal_user, portal_password)
    if df == 'cases':
        # Generate new CSV files while we're at it.
        # In production they will be written to the "capacity" webserver
        # In a test environment they end up in the local folder.
        results_df = FeatureLayer(cases_url).query(where="editor='EMD'", order_by_fields="utc_date DESC",
                                return_all_records=False, result_record_count=1, return_geometry=False).sdf
    elif df == 'ppe':
        results_df = FeatureLayer(ppe_url).query(where="facility='Clatsop'", order_by_fields="utc_date DESC",
                                return_all_records=False, result_record_count=1, return_geometry=False).sdf
    else:
        results_df = pd.DataFrame()
    return render_template('thanks.html', df=results_df)

@main.route('/', methods=['GET'])
def home_page():
    return render_template('home.html')

def update_cases(layer):
    """
        Read from server and write to CSV file
    """
    try:
        sdf = pd.DataFrame.spatial.from_layer(layer)
        # We're only interested in data manually entered for Clatsop
        emd_df = sdf[sdf.editor == 'EMD']

        # This will generate two CSV files in the "cases" subdirectory
        # which will be mounted from Docker to put the files into
        # the "capacity" server.
        # I no longer use the CSV files,
        # generate_chart reads the feature class now.
        #csv_exporter(emd_df, "cases")

        fig = generate_chart()
        fig.write_html("cases/index.html")

    except Exception as e:
        error = e
        print("CSV update failed.", e)
        return False
    return True

@main.route('/cases', methods=['GET', 'POST'])
def cases_entry_form():
    global error

    portal_url = current_app.config['PORTAL_URL']
    portal_user = current_app.config['PORTAL_USER']
    portal_password = current_app.config['PORTAL_PASSWORD']

    cases_url = current_app.config['COVID_CASES_URL']

    form = CasesForm()
    if form.validate_on_submit():

        # We've received input from a form, process it.
        #session['name'] = form.name.data

        try:
            local = parsetime(form.datestamp.data)
            utc = local2utc(local).strftime(time_format)
        except Exception as e:
            print("Time format is confusing to me.", e)
            error = e
            return redirect("/fail")

        try:
            n = {
                "attributes": {
                    "utc_date":        utc,
                    "last_update":     utc,
                    'name':            'Clatsop',
                    "total_cases":     s2i(form.total_cases.data),
                    "new_cases":       s2i(form.new_cases.data),
                    "total_negative":  s2i(form.negative.data),

                    "total_tests":     s2i(form.total_cases.data) + s2i(form.negative.data),
                    
                    "total_deaths":    s2i(form.total_deaths.data),
                    "new_deaths":      s2i(form.new_deaths.data),

                    "source":          VERSION,
                    "editor":          "EMD",
                },
                "geometry": county_centroid
            }
        except Exception as e:
            print("Attribute error.", e)
            error = e
            return redirect("/fail")

        # write back to server

        results = ''
        try:
            portal = GIS(portal_url, portal_user, portal_password)
            layer = FeatureLayer(cases_url)
            print(layer, n)
            results = layer.edit_features(adds=[n])

        except Exception as e:
            error = e
            print("Write failed.", e, results)
            return redirect("/fail")

        if not update_cases(layer):
            return redirect("/fail")

        return redirect('/thanks/cases')

    # Create a data entry form

    try:
        portal = GIS(portal_url, portal_user, portal_password)
        df = FeatureLayer(cases_url).query(where="name='Clatsop' AND editor='EMD'", order_by_fields="utc_date DESC").sdf
        s = df.iloc[0]
        print(s)
    except Exception as e:
        print("Reading old data failed.", e)
        pass

    try:
        # Force the old date into UTC
        old_date = s['utc_date'].replace(tzinfo=timezone('UTC'))
        # Show the old date in the local TZ
        form.old_date = "(previous %s)" % old_date.astimezone(
            timezone('America/Los_Angeles')).strftime(time_format)
    except Exception as e:
        print("Converting old date stamp failed.", e)
        pass

    try:
        form.total_cases.data  = s['total_cases']
        form.new_cases.data    = s['new_cases']
        form.negative.data     = s['total_negative']
        #form.recovered.data    = s['total_recovered']
        form.total_deaths.data = s['total_deaths']
        form.new_deaths.data   = s['new_deaths']
        #form.editor.data      = s['editor']
    except Exception as e:
        print("Filling in form failed.", e)
        pass

    now = datetime.now()
    ds = now.strftime(time_format)
    form.datestamp.data = ds

    return render_template('cases.html', form=form)

def s2i(s):
    """ Convert a string to an integer even if it has + and , in it. """
    if s == None or s == '':
        return None
    if type(s) == type(0):
        # This is already an integer
        return s
    if s:
        return int(float(s.replace(',', '')))
    return None

def s2f(s):
    """ Convert a string to a float even if it has + and , in it. """
    if s == None or s == '':
        return None
    if type(s) == type(0.0) or type(s) == type(0):
        # Already a number
        return s
    if s:
        return float(s.replace(',', ''))
    return None

def percent(n,d):
    if n and d:
        fn = s2f(n)
        fd = s2f(d)
        if fd != 0:
            return round(fn * 100.0 / fd, 0)
    return 0

@main.route('/ppe/<facility>', methods=['GET', 'POST'])
def update_ppe(facility="Clatsop"):
    global error

    portal_url = current_app.config['PORTAL_URL']
    portal_user = current_app.config['PORTAL_USER']
    portal_password = current_app.config['PORTAL_PASSWORD']

    ppe_url   = current_app.config['PPE_INVENTORY_URL']

    if not facility in ['Clatsop', 'PSH', 'CMH']:
        error = 'Could not recognize the facilty name'
        return redirect('/fail')

    form = PPEForm()
    if form.validate_on_submit():
        # We have INPUT and now we're going to SAVE it.

        #session['name'] = form.name.data

        try:
            # The form has local times and we need UTC
            local = parsetime(form.datestamp.data)
            utc_now = local2utc(local).strftime(time_format)
        except Exception as e:
            print("Time format is confusing to me.", e)
            error = e
            return redirect("/fail")

        if facility == 'Clatsop':
            utc_updated = utc_now
        else:
            try:
                # The form has local times and we need UTC
                local = parsetime(form.updated.data)
                utc_updated = local2utc(local).strftime(time_format)
            except Exception as e:
                print("Time format is confusing to me.", e)
                utc_updated = utc_now

        try:
            n = {"attributes": {
                "utc_date":        utc_now,
                "editor":          VERSION,
                'facility':        facility,

                "n95_date":        utc_updated,
                "n95":             s2i(form.n95.data),
                "n95_burn":        s2i(form.n95_burn.data),
                "n95_goal":        s2i(form.n95_goal.data),
                "n95_complete":    percent(form.n95.data, form.n95_goal.data),

                "mask_date":       utc_updated,
                "mask":            s2i(form.mask.data),
                "mask_burn":       s2i(form.mask_burn.data),
                "mask_goal":       s2i(form.mask_goal.data),
                "mask_complete":   percent(form.mask.data, form.mask_goal.data),

                "shield_date":     utc_updated,
                "shield":          s2f(form.shield.data),
                "shield_burn":     s2f(form.shield_burn.data),
                "shield_goal":     s2f(form.shield_goal.data),
                "shield_complete": percent(form.shield.data, form.shield_goal.data),

                "glove_date":      utc_updated,
                "glove":           s2i(form.glove.data),
                "glove_burn":      s2i(form.glove_burn.data),
                "glove_goal":      s2i(form.glove_goal.data),
                "glove_complete":  percent(form.glove.data, form.glove_goal.data),

                "gown_date":       utc_updated,
                "gown":            s2i(form.gown.data),
                "gown_burn":       s2i(form.gown_burn.data),
                "gown_goal":       s2i(form.gown_goal.data),
                "gown_complete":   percent(form.gown.data, form.gown_goal.data),

                "coverall_date":   utc_updated,
                "coverall":        s2i(form.coverall.data),
                "coverall_burn":   s2i(form.coverall_burn.data),
                "coverall_goal":   s2i(form.coverall_goal.data),
                "coverall_complete": percent(form.coverall.data, form.coverall_goal.data),

                "sanitizer_date":  utc_updated,
                "sanitizer":       s2f(form.sanitizer.data),
                "sanitizer_burn":  s2f(form.sanitizer_burn.data),
                "sanitizer_goal":  s2f(form.sanitizer_goal.data),
                "sanitizer_complete":  percent(form.sanitizer.data, form.sanitizer_goal.data),

                "goggle_date":     utc_updated,
                "goggle":          s2i(form.goggle.data),
                "goggle_burn":     s2i(form.goggle_burn.data),
                "goggle_goal":     s2i(form.goggle_goal.data),
                "goggle_complete": percent(form.goggle.data, form.goggle_goal.data),

            },
                "geometry": county_centroid
            }
        except Exception as e:
            print("Attribute error.", e)
            error = e
            return redirect("/fail")

        results = ''
        try:
            portal = GIS(portal_url, portal_user, portal_password)
            layer = FeatureLayer(ppe_url)
            print(layer, n)
            #results = layer.edit_features(adds=[n])
            del portal
        except Exception as e:
            error = str(e) + ' -- make sure the layer is owned by sde not DBO'
            print("Write failed", e)
            return redirect("/fail")

        return redirect('/thanks/ppe')

    # We need input so we're sending the form.

    try:
        # Try to populate the form with the newest values
        portal = GIS(portal_url, portal_user, portal_password)
        layer = FeatureLayer(ppe_url)
        df = pd.DataFrame.spatial.from_layer(layer)
        #print(df)
        del portal

        ppe_df = df[df.facility == facility]
        #print(ppe_df)
        newest = ppe_df.sort_values(
            by=['utc_date'], ascending=False).head(1)
#        print("QUERY SORTED BY date", newest)
        s = newest.iloc[0]
        print("QUERY RESULTS")
        print(s)

        # Force the old date into UTC
        old_date = s['utc_date'].replace(tzinfo=timezone('UTC'))
        # Show the old date in the local TZ
        form.old_date = "(previous %s)" % old_date.astimezone(
            timezone('America/Los_Angeles')).strftime(time_format)

        if facility != 'Clatsop':
            old_date = s['n95_date'].replace(tzinfo=timezone('UTC'))
            # Show the old date in the local TZ
            form.updated.data = old_date.astimezone(
                timezone('America/Los_Angeles')).strftime(time_format)

        form.facility.data = s['facility']
        
        form.n95.data = s['n95']
        form.n95_burn.data = s['n95_burn']
        form.n95_goal.data = s['n95_goal']
        form.n95_complete.data = s['n95_complete']

        form.mask.data = s['mask']
        form.mask_burn.data = s['mask_burn']
        form.mask_goal.data = s['mask_goal']
        form.mask_complete.data = s['mask_complete']

        form.shield.data = s['shield']
        form.shield_burn.data = s['shield_burn']
        form.shield_goal.data = s['shield_goal']
        form.shield_complete.data = s['shield_complete']

        form.glove.data = s['glove']
        form.glove_burn.data = s['glove_burn']
        form.glove_goal.data = s['glove_goal']
        form.glove_complete.data = s['glove_complete']

        form.gown.data = s['gown']
        form.gown_burn.data = s['gown_burn']
        form.gown_goal.data = s['gown_goal']
        form.gown_complete.data = s['gown_complete']

        form.sanitizer.data = s['sanitizer']
        form.sanitizer_burn.data = s['sanitizer_burn']
        form.sanitizer_goal.data = s['sanitizer_goal']
        form.sanitizer_complete.data = s['sanitizer_complete']

        form.goggle.data = s['goggle']
        form.goggle_burn.data = s['goggle_burn']
        form.goggle_goal.data = s['goggle_goal']
        form.goggle_complete.data = s['goggle_complete']

        form.coverall.data = s['coverall']
        form.coverall_burn.data = s['coverall_burn']
        form.coverall_goal.data = s['coverall_goal']
        form.coverall_complete.data = s['coverall_complete']

    except Exception as e:
        print("Reading old data failed.", e)
        pass

    # Show the current local time in the form.
    now = datetime.now()
    ds = now.strftime(time_format)
    form.datestamp.data = ds

    html = 'ppe_hoscap.html'
    if facility == 'Clatsop':
        html = 'ppe.html'

    return render_template(html, form=form)

# That's all!
