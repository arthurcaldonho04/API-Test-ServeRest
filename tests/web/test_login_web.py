"""Casos de teste de interface: login."""
import re

import pytest
from playwright.sync_api import Page, expect

from pages.admin_page import HomeAdminPage
from pages.home_cliente_page import HomeClientePage
from pages.login_page import LoginPage

pytestmark = pytest.mark.web


def test_ct_web_01_login_administrador(page: Page, admin):
    LoginPage(page).abrir().entrar(admin["email"], admin["password"])

    expect(page).to_have_url(re.compile(r"/admin/home$"))
    expect(HomeAdminPage(page).boas_vindas).to_contain_text(admin["nome"])


def test_ct_web_02_login_cliente(page: Page, cliente):
    LoginPage(page).abrir().entrar(cliente["email"], cliente["password"])

    expect(page).to_have_url(re.compile(r"/home$"))
    expect(HomeClientePage(page).titulo).to_be_visible()


def test_ct_web_03_login_com_senha_incorreta(page: Page, cliente):
    login = LoginPage(page).abrir()

    login.entrar(cliente["email"], "senha_errada")

    expect(login.alerta_erro).to_contain_text("Email e/ou senha inválidos")
    expect(page).to_have_url(re.compile(r"/login$"))


def test_ct_web_04_acesso_sem_login_redireciona(page: Page):
    page.goto("/home")

    expect(page).to_have_url(re.compile(r"/login$"))


def test_ct_web_05_logout(page: Page, cliente):
    LoginPage(page).abrir().entrar(cliente["email"], cliente["password"])
    home = HomeClientePage(page)
    expect(home.titulo).to_be_visible()

    home.botao_logout.click()

    expect(page).to_have_url(re.compile(r"/login$"))
