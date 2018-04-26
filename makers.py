'''
This file is part of STIX 2.0 UoM Editor.

STIX 2.0 UoM Editor is free software: you can redistribute it and/or modify

it under the terms of the GNU General Public License as published by

the Free Software Foundation, either version 3 of the License, or

(at your option) any later version.

STIX 2.0 UoM Editor is distributed in the hope that it will be useful,

but WITHOUT ANY WARRANTY; without even the implied warranty of

MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the

GNU General Public License for more details.

You should have received a copy of the GNU General Public License

along with STIX 2.0 UoM Editor.  If not, see <http://www.gnu.org/licenses/>.
'''
import stix2
from stix_io import itemtofile

def attack_pattern_maker(**kwargs):
    attack_pattern = stix2.AttackPattern(**kwargs)
    flag = itemtofile(attack_pattern)
    return flag, attack_pattern


def campaign_maker(**kwargs):
    campaign = stix2.Campaign(**kwargs)
    flag = itemtofile(campaign)
    return flag, campaign


def course_of_action_maker(**kwargs):
    coa = stix2.CourseOfAction(**kwargs)
    flag = itemtofile(coa)
    return flag, coa


def identity_maker(**kwargs):
    identity = stix2.Identity(**kwargs)
    flag = itemtofile(identity)
    return flag, identity


def indicator_maker(**kwargs):
    indicator =  stix2.Indicator(**kwargs)
    flag = itemtofile(indicator)
    return flag, indicator


def intrusion_set_maker(**kwargs):
    intrusion_set = stix2.IntrusionSet(**kwargs)
    flag = itemtofile(intrusion_set)
    return flag, intrusion_set


def malware_maker(**kwargs):
    malware = stix2.Malware(**kwargs)
    flag = itemtofile(malware)
    return flag, malware


def observed_data_maker(**kwargs):
    observed_data = stix2.ObservedData(**kwargs)
    flag = itemtofile(observed_data)
    return flag, observed_data

def report_maker(**kwargs):
    report = stix2.Report(**kwargs)
    flag = itemtofile(report)
    return flag, report


def threat_actor_maker(**kwargs):
    threat_actor = stix2.ThreatActor(**kwargs)
    flag = itemtofile(threat_actor)
    return flag, threat_actor


def tool_maker(**kwargs):
    tool = stix2.Tool(**kwargs)
    flag = itemtofile(tool)
    return flag, tool


def vulnerability_maker(**kwargs):
    vulnerability = stix2.Vulnerability(**kwargs)
    flag = itemtofile(vulnerability)
    return flag, vulnerability

def relationship_maker(source,type,target):
    relationship=stix2.Relationship(source,type,target)
    itemtofile(relationship)
    return relationship

def marking_definition_maker(**kwargs):
    marking_definition = stix2.MarkingDefinition(**kwargs)
    flag = itemtofile(marking_definition)
    return flag, marking_definition
